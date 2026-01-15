from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from app.schemas.diet import DietRequest, DietResponse
from app.core.database import database
from app.routers.auth import get_current_user  # 👈 Import enabled!
from app.ml.predictor import predict_diet_plan # 👈 Uses your ML helper

router = APIRouter(
    prefix="/diet",
    tags=["Diet Planner"]
)

# --- HELPER FUNCTIONS ---
def calculate_bmi(weight, height):
    # Prevent division by zero
    if height <= 0: return 0, "Unknown"
    
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
    current_user: dict = Depends(get_current_user) # 🔒 Security enabled
):
    # 1. Calculate Health Stats
    bmi, bmi_category = calculate_bmi(request.weight, request.height)
    age_group = get_age_group(request.age)

    # 2. PREDICTION LOGIC (Using the Helper)
    # This automatically handles the ML model OR falls back to rules if model fails
    diet_text, avoid_text, calories = predict_diet_plan(
        age_group=age_group,
        bmi_category=bmi_category,
        disease=request.disease
    )

    # 3. Fallback Safety (Just in case ML returns nothing)
    if not diet_text:
        if "diabetes" in request.disease.lower():
            diet_text = "Low Sugar, High Fiber"
            avoid_text = "Sugar, White Rice, Fruit Juices"
            calories = 1600
        elif "hypertension" in request.disease.lower():
            diet_text = "DASH Diet (Low Sodium)"
            avoid_text = "Salt, Pickles, Canned Soup"
            calories = 1500
        else:
            diet_text = "Balanced Healthy Diet"
            avoid_text = "Junk Food, Deep Fried Items"
            calories = 1800

    # Ensure avoid_text is a list for the Frontend
    avoid_list = avoid_text.split(",") if isinstance(avoid_text, str) else [avoid_text]

    # 4. Save to MongoDB History
    # We do this AFTER we have the results
    history_entry = {
        "user_id": current_user["_id"],
        "timestamp": datetime.utcnow(),
        "input": request.dict(),
        "output": {
            "diet_type": diet_text,
            "calories": calories,
            "avoid_foods": avoid_list,
            "bmi": bmi
        }
    }
    
    # Use the correct collection name (diet_plans_collection or similar)
    # Assuming 'diet_plans' based on your database.py
    await database.get_collection("diet_plans").insert_one(history_entry)

    # 5. Return Response
    return {
        "diet_type": diet_text,
        "calories": calories,
        "avoid_foods": avoid_list,
        "bmi_value": bmi,
        "bmi_category": bmi_category,
        "message": f"Plan generated successfully for {request.disease}"
    }