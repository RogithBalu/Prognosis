from pydantic import BaseModel
from typing import List, Optional

class DietRequest(BaseModel):
    age: int
    weight: float      # in kg
    height: float      # in cm
    disease: str       # e.g., "diabetes"
    gender: str = "Any"
    activity_level: Optional[str] = "Moderate"

class DietResponse(BaseModel):
    diet_type: str
    calories: int
    avoid_foods: List[str]
    bmi_value: float
    bmi_category: str
    message: str