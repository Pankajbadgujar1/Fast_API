from fastapi import FastAPI,Path, HTTPException, Query
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
from fastapi.responses import JSONResponse
app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description=" ID of the patient ", example="P001")]  
    name:Annotated[str, Field(..., description=" Name of the patient ", example="John Doe")]
    city:Annotated[str, Field(..., description=" City of the patient ", example="New York")]
    age:Annotated[int, Field(...,gt=0,lt=120, description=" Age of the patient ", example=40)]
    gender:Annotated[Literal['Male', 'Female', 'Other'], Field(..., description=" Gender of the patient ", example="Male")]
    height:Annotated[float, Field(...,gt=0, description=" Height of the patient in meters ", example=1.75 )]
    weight:Annotated[float, Field(..., description=" Weight of the patient in kgs ", example=70.5)]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        bmi = self.bmi
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

def load_data():
    with open("patients.json", "r") as file:
        data = json.load(file)
    return data

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {"message": "Hello, World!"}

@app.get("/about")
def about():
    return {"message": "A fully functional API  to manage patient records."}

@app.get("/view")
def view():
    data = load_data()
    return data 

# Learn Path parameter and Query parameter

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description='Id of the patient in the Database', example='P001') ):

    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")


    #Query Parameter Example

@app.get('/sort')
def sort_patients(
    sort_by: str = Query(..., description="Sort on the basis of height, weight and bmi"),
    order: str = Query("asc", description="Sort order: asc or desc order")
):
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by field. Must be one of {valid_fields}")

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order. Must be 'asc' or 'desc'")

    data = load_data()
    sort_order = True if order == "desc" else False
    sorted_items = sorted(data.items(), key=lambda item: item[1].get(sort_by, 0), reverse=sort_order)
    # return as list of (id, dict) tuples or convert to a list of dicts including id:
    return [{ "id": pid, **info } for pid, info in sorted_items]


@app.post("/create")
def create_patient(patient: Patient):
    # Load existing data
    # check if patient already exists
    # if exists, raise error
    # else add new patient and save to file

    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists.")
    
    #data[patient.id] = patient.dict()
    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)
    
    return JSONResponse(status_code=201, content={"message": "Patient record created successfully."})