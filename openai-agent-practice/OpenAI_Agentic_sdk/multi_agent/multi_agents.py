
from agents import Agent
from agents_configurations.agent_config import GEMINI_MODEL 
from schemas.pythone_tutor import PythonTutorSchema

gemini_agent = Agent(
    name="Python Tutor",
    instructions="You are a helpful coding assistant that helps people learn Python programming. "
                 "You provide clear explanations and code examples to help users understand Python concepts.",
    model=GEMINI_MODEL,
    output_type=PythonTutorSchema
    )