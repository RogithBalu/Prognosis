from fastapi import APIRouter, HTTPException
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.ml_services import predict_diet_and_calories
from app.schemas.prediction import PredictionRequest, PredictionResponse

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict(data: PredictionRequest):
    """
    Predict daily calories and diet recommendations
    """
    try:
        result = predict_diet_and_calories(data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
