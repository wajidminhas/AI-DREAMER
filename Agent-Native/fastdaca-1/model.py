


from pydantic import BaseModel, Field


class Patient(BaseModel):
    name: str
    age: int = Field(gt=10, lt=120, description="Age of the patient must be between 10 and 120")
    gender: str