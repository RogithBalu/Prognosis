import pickle
import numpy as np
import os

# 1. Define Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "diet_classifier.pkl")

# 2. Global variable to hold the model
_model_data = {}

def load_model():
    """Loads the model and encoders into memory only once."""
    global _model_data
    if not _model_data and os.path.exists(MODEL_PATH):
        try:
            with open(MODEL_PATH, "rb") as f:
                _model_data = pickle.load(f)
            print("✅ ML Model loaded successfully.")
        except Exception as e:
            print(f"❌ Error loading ML model: {e}")

# 3. Helper to safe-encode inputs
def safe_transform(encoder, value):
    """Handles cases where the user sends a disease name the model hasn't seen."""
    try:
        return encoder.transform([value])[0]
    except ValueError:
        # Fallback: if unknown disease, map to a default (e.g., first class)
        # or raise an error. Here we default to index 0 safely.
        return 0 

def predict_diet_plan(age_group: str, bmi_category: str, disease: str):
    """
    Input: "Adult", "Overweight", "Diabetes"
    Output: "Low Sugar Diet", "Sugar, Rice", 1800 (Calories is mocked)
    """
    # Load if not loaded
    if not _model_data:
        load_model()
    
    if not _model_data:
        return None, None, None # Model failed to load

    model = _model_data["model"]
    encoders = _model_data["encoders"]

    # 1. Prepare Input (Encode text -> numbers)
    # The model expects: [Age_Group, BMI_Category, Disease]
    try:
        age_encoded = safe_transform(encoders["Age_Group"], age_group)
        bmi_encoded = safe_transform(encoders["BMI_Category"], bmi_category)
        disease_encoded = safe_transform(encoders["Disease"], disease)
        
        input_vector = np.array([[age_encoded, bmi_encoded, disease_encoded]])

        # 2. Predict (Returns list of [Diet_Index, Avoid_Index])
        prediction = model.predict(input_vector)
        
        # prediction is [[Diet_Val, Avoid_Val]]
        diet_idx = prediction[0][0]
        avoid_idx = prediction[0][1]

        # 3. Decode Output (Numbers -> Text)
        diet_text = encoders["Recommended_Diet"].inverse_transform([diet_idx])[0]
        avoid_text = encoders["Avoid_Food"].inverse_transform([avoid_idx])[0]
        
        # 4. Handle Calories (Since model doesn't predict it)
        # We estimate based on BMI for now
        calories = 1500 if bmi_category == "Obese" else 1800 if bmi_category == "Overweight" else 2200

        return diet_text, avoid_text, calories

    except Exception as e:
        print(f"Prediction logic error: {e}")
        return None, None, None