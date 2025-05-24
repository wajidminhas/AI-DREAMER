

from fastapi import FastAPI

from model import Patient


app : FastAPI = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}                                                                                                                                                                                                                                               
    
@app.post('/view/patient')
async def view_patient(patient: Patient):
    print(patient)
    return {"patient": f"Mr/Ms {patient.name} is under observation"}
