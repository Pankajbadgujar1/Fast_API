from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from model.predict import predict_output, MODEL_VERSION,model
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse

app = FastAPI()
@app.post("/predict" , response_model=PredictionResponse)
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

    input_data = {
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": norm_occ,
    }
    try:
        prediction = predict_output(input_data)
        return JSONResponse(status_code=200 , content={'predicted_category': prediction })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

@app.get('/')
def home():
    return {"message": "Welcome to the Insurance Premium Prediction API"}

@app.get("/health")
def health_check():
    return {"status": "ok", "version": MODEL_VERSION}