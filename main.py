from fastapi import FastAPI,Path
import json

app = FastAPI()

def load_data():
    with open("patients.json", "r") as file:
        data = json.load(file)
    return data

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
    else:
        return {"error": "Patient not found"}