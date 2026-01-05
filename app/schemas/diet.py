from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
import pandas as pd
import numpy as np
import pickle
import os

# Import your modules
from app.schemas.diet import DietRequest, DietResponse
from app.core.database import database  # Your MongoDB connection
from app.routers.auth import get_current_user # To secure the endpoint

router = APIRouter(
    prefix="/diet",
    tags=["Diet Planner"]
)

# --- ML MODEL LOADER (The "Brain") ---
# Try to load the model if it exists, otherwise use a fallback
MODEL_PATH = "app/ml/diet_model.pkl"
model_data = None

if os.path.exists(MODEL_PATH):
    try:
        with open(MODEL_PATH, "rb") as f:
            model_data = pickle.load(f)
        print("✅ ML Model loaded successfully.")
    except Exception as e:
        print(f"⚠️ Error loading ML model: {e}")

# --- HELPER FUNCTIONS ---
def calculate_bmi(weight, height):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    
    if bmi < 18.5: category = "Underweight"
    elif bmi < 24.9: category = "Normal"
    elif bmi < 29.9: category = "Overweight"
    else: category = "Obese"
    
    return round(bmi, 1), category

def get_age_group(age):
    if age < 20: return "Teen"
    elif age < 60: return "Adult"
    return "Senior"

# --- THE ENDPOINT ---
@router.post("/predict", response_model=DietResponse)
async def generate_diet_plan(
    request: DietRequest, 
    current_user: dict = Depends(get_current_user) # 🔒 Protect this route
):
    # 1. Calculate Health Stats
    bmi, bmi_category = calculate_bmi(request.weight, request.height)
    age_group = get_age_group(request.age)

    # 2. PREDICTION LOGIC
    # Scenario A: If ML Model is ready, use it
    if model_data:
        try:
            # Prepare input vector (Matches training data)
            # You might need to update this part once ML team gives final specs
            disease_code = model_data["le_disease"].transform([request.disease])[0]
            age_code = model_data["le_age_group"].transform([age_group])[0]
            bmi_code = model_data["le_bmi"].transform([bmi_category])[0]
            
            input_vector = np.array([[disease_code, age_code, bmi_code]])
            
            # Predict
            pred_diet_code = model_data["model_diet"].predict(input_vector)[0]
            pred_avoid_code = model_data["model_avoid"].predict(input_vector)[0]
            pred_calories = model_data["model_calories"].predict(input_vector)[0]
            
            # Decode
            diet_type = model_data["le_diet"].inverse_transform([pred_diet_code])[0]
            avoid_foods = model_data["le_avoid"].inverse_transform([pred_avoid_code])[0]
            calories = int(pred_calories)
            
        except Exception as e:
            # Fallback if model fails specific prediction
            print(f"Prediction Error: {e}")
            diet_type = "Balanced Diet (Model Error)"
            avoid_foods = "Processed Foods"
            calories = 2000

    # Scenario B: Fallback (Rule-Based) - Use this until ML team is ready
    else:
        # Simple logic so Frontend doesn't break
        if "diabetes" in request.disease.lower():
            diet_type = "Low Sugar, High Fiber"
            avoid_foods = "Sugar, White Rice, Fruit Juices"
            calories = 1600
        elif "hypertension" in request.disease.lower():
            diet_type = "DASH Diet (Low Sodium)"
            avoid_foods = "Salt, Pickles, Canned Soup"
            calories = 1500
        else:
            diet_type = "Balanced Healthy Diet"
            avoid_foods = "Junk Food, Deep Fried Items"
            calories = 1800

    # 3. Save to MongoDB History
    # We store the inputs + outputs + user_id
    history_entry = {
        "user_id": current_user["_id"],
        "timestamp": datetime.utcnow(),
        "input": request.dict(),
        "output": {
            "diet_type": diet_type,
            "calories": calories,
            "avoid_foods": avoid_foods,
            "bmi": bmi
        }
    }
    await database.diet_history.insert_one(history_entry)

    # 4. Return Response
    return {
        "diet_type": diet_type,
        "calories": calories,
        "avoid_foods": avoid_foods.split(",") if isinstance(avoid_foods, str) else avoid_foods,
        "bmi_value": bmi,
        "bmi_category": bmi_category,
        "message": f"Plan generated successfully for {request.disease}"
    }