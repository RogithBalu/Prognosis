from pydantic import BaseModel

# Input for prediction
class PredictionRequest(BaseModel):
    age_group: str
    bmi_category: str
    disease: str

# Output for prediction
class PredictionResponse(BaseModel):
    calories_per_day: int
    recommended_diet: str
    avoid_food: str
