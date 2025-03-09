from fastapi import FastAPI
import joblib  # For loading the trained model
import numpy as np
from pydantic import BaseModel

# Load your trained model (ensure it's uploaded in the same directory as this script)
model = joblib.load("model.pkl")  # Change filename if needed

# Initialize FastAPI app
app = FastAPI()

# Define input schema using Pydantic
class ModelInput(BaseModel):
    Price: float
    Category_Beauty: int
    Category_Books: int
    Category_Electronics: int
    Category_Fashion: int
    Category_Home: int
    Level_high: int  # Always 1
    Level_low: int
    Level_normal: int

# MinMax normalization for price
PRICE_MIN = 0  # Set actual min price from training data
PRICE_MAX = 1000  # Set actual max price from training data

def normalize_price(price):
    return (price - PRICE_MIN) / (PRICE_MAX - PRICE_MIN)

@app.post("/predict")
def predict(data: ModelInput):
    # Preprocess input
    normalized_price = normalize_price(data.Price)
    
    # Create feature array
    input_data = np.array([
        normalized_price,data.Category_Beauty, data.Category_Books,
        data.Category_Electronics, data.Category_Fashion, data.Category_Home,
        data.Level_high, data.Level_low, data.Level_normal
    ]).reshape(1, -1)
    
    # Get prediction
    prediction = model.predict(input_data)
    
    return {"predicted_month": int(prediction[0])}
