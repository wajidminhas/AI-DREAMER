


from pydantic import BaseModel

class PythonTutorSchema(BaseModel):
    code: str
    input: str
    explanation: str
    output: str