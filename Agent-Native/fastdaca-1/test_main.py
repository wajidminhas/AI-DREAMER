from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_view_patient():
    patient_data = {
        "name": "John Doe",
        "age": 30,
        "gender": "male"
    }
    response = client.post("/view/patient", json=patient_data)
    assert response.status_code == 200
    assert response.json() == {"patient": "Mr/Ms John Doe is under observation"}

