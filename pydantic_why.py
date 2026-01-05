from pydantic import BaseModel
from typing import List, Dict, Optional

class Patient(BaseModel):
    name: str
    age: int 
    weight: float
    married: bool = False
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print("inserted data")

patient_info = {"name": 'John', "age": "40" , "weight": 70.5, "married": True,
                  "contact_details": {"email": "john@example.com", "phone": "123-456-7890"}}

patient = Patient(**patient_info)

insert_patient_data(patient)