# app/services/ml_services.py

import pickle
import numpy as np

# global variables
calorie_model = None
diet_model = None
age_encoder = None
bmi_encoder = None
disease_encoder = None
encoders = None

def load_models():
    global calorie_model, diet_model, age_encoder, bmi_encoder, disease_encoder, encoders

    # Load calorie regressor
    with open("mlmodel/calorie_regressor.pkl", "rb") as f:
        calorie_bundle = pickle.load(f)
    calorie_model = calorie_bundle["model"]
    age_encoder = calorie_bundle["age_encoder"]
    bmi_encoder = calorie_bundle["bmi_encoder"]
    disease_encoder = calorie_bundle["disease_encoder"]

    # Load diet classifier
    with open("mlmodel/diet_classifier.pkl", "rb") as f:
        diet_bundle = pickle.load(f)
    diet_model = diet_bundle["model"]
    encoders = diet_bundle["encoders"]

# Call this once at startup
load_models()

def predict_diet_and_calories(data):
    try:
        age = age_encoder.transform([data.age_group])[0]
        bmi = bmi_encoder.transform([data.bmi_category])[0]
        disease = disease_encoder.transform([data.disease])[0]
    except ValueError:
        raise ValueError("Invalid input values. Check Age_Group, BMI_Category, Disease.")

    X = np.array([[age, bmi, disease]])

    calories = int(calorie_model.predict(X)[0])

    diet_pred = diet_model.predict(X)[0]
    recommended_diet = encoders["Recommended_Diet"].inverse_transform([diet_pred[0]])[0]
    avoid_food = encoders["Avoid_Food"].inverse_transform([diet_pred[1]])[0]

    return {
        "calories_per_day": calories,
        "recommended_diet": recommended_diet,
        "avoid_food": avoid_food
    }
