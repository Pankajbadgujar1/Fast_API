from fastapi import FastAPI,Path, HTTPException, Query
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