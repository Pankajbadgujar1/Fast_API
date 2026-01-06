from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, computed_field, Field
from typing import Literal, Annotated
import pickle
import pandas as pd

model = None
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
except Exception as e:
    print("Warning: failed to load model.pkl:", e)

app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]
# pydantic model to validate incoming data

class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120, description=" Age of the user ")]
    weight: Annotated[float, Field(..., gt=0, description=" Weight of the user in kgs ", example=70.5)]
    height: Annotated[float, Field(..., gt=0, description=" Height of the user in meters ", example=1.75)]
    income_lpa: Annotated[float, Field(..., gt=0, description=" Income of the user in lakhs per annum ", example=5.0)]
    smoker: Annotated[bool, Field(..., description=" Whether the user is a smoker or not ", example=False)]
    city: Annotated[str, Field(..., description=" City of the user ", example="New York")]
    occupation: Annotated[str, Field(..., description=" Occupation of the user ", example="salaried")]
      
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi  

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3

@app.post("/predict")
def predict_premium(data: UserInput):
    # normalize occupation synonyms to the allowed categories
    _occ_map = {
        "salaried": "private_job",
        "salary": "private_job",
        "govt": "government_job",
        "government": "government_job",
    }
    occ_raw = str(data.occupation).strip().lower()
    norm_occ = _occ_map.get(occ_raw, occ_raw)
    valid_occs = {"retired", "freelancer", "student", "government_job", "unemployed", "business_owner", "private_job"}
    if norm_occ not in valid_occs:
        raise HTTPException(status_code=400, detail=f"Invalid occupation. Must be one of {sorted(valid_occs)}")

    input_data = pd.DataFrame([{
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": norm_occ,
    }])
    

    prediction = model.predict(input_data)[0]
    return JSONResponse(status_code=200 , content={'predicted_category': prediction })



