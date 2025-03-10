from fastapi import FastAPI
import joblib  
import numpy as np
from pydantic import BaseModel

model = joblib.load("model.pkl")  

#  FastAPI app
app = FastAPI()

# Define input schema using Pydantic
class ModelInput(BaseModel):
    Price: float
    Category_Beauty: int
    Category_Books: int
    Category_Electronics: int
    Category_Fashion: int
    Category_Home: int
    Level_high: int  
    Level_low: int
    Level_normal: int

# MinMax normalization for price
PRICE_MIN = 2300  
PRICE_MAX = 150000  

def normalize_price(price):
    return (price - PRICE_MIN) / (PRICE_MAX - PRICE_MIN)

@app.post("/predict")
def predict(data: ModelInput):
    normalized_price = normalize_price(data.Price)
    #  feature array
    input_data = np.array([
        normalized_price,data.Category_Beauty, data.Category_Books,
        data.Category_Electronics, data.Category_Fashion, data.Category_Home,
        data.Level_high, data.Level_low, data.Level_normal
    ]).reshape(1, -1)
    
    prediction = model.predict(input_data)
    return {"predicted_month": int(prediction[0])}
