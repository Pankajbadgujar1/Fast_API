from pydantic import BaseModel, computed_field, Field, field_validator
from typing import Literal, Annotated

from config.city_tire import tier_1_cities, tier_2_cities

# pydantic model to validate incoming data

class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120, description=" Age of the user ")]
    weight: Annotated[float, Field(..., gt=0, description=" Weight of the user in kgs ", example=70.5)]
    height: Annotated[float, Field(..., gt=0, description=" Height of the user in meters ", example=1.75)]
    income_lpa: Annotated[float, Field(..., gt=0, description=" Income of the user in lakhs per annum ", example=5.0)]
    smoker: Annotated[bool, Field(..., description=" Whether the user is a smoker or not ", example=False)]
    city: Annotated[str, Field(..., description=" City of the user ", example="New York")]
    occupation: Annotated[str, Field(..., description=" Occupation of the user ", example="salaried")]


    @field_validator('city')
    @classmethod
    def validate_city(cls, v: str) -> str:
        v = v.strip().title()
        return v
          
        

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