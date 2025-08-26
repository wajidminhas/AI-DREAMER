

from agents import Agent
from configurations.config import gemini_model
from my_tools.my_tools import fetch_users, fetch_user_by_id

api_agent : Agent = Agent(
    name= "API Assistent",
    instructions="you are a helpful Assitent, reply the user query with gently",
    model=gemini_model, 
    tools = [fetch_users, fetch_user_by_id]
)

general_agent: Agent = Agent(
    name= "General Agent",
    instructions = "you are General agent who reply user query and if necessrory use the tools to give the data",
    model = gemini_model,
    tools = [api_agent.as_tool(
        tool_name="API_Agent",
        tool_description="use this tool to get the data of user from jsonplaceholder api"
    )]
)