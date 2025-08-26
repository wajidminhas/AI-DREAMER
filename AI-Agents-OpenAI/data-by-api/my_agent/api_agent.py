

from agents import Agent
from configurations.config import gemini_model
from my_tools.my_tools import fetch_users, fetch_user_by_id

gen_agent : Agent = Agent(
    name= "Assistent",
    instructions="you are a helpful Assitent, reply the user query with gently",
    model=gemini_model, 
    tools = [fetch_users, fetch_user_by_id]
)