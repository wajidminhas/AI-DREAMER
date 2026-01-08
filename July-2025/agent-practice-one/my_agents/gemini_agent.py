from agents import Agent
from agent_configuration.agents_config import model
from tools.weather_agent import get_weather
from tools.location_agent import get_location


agent : Agent = Agent(
    name = "Heplful Assistant",
    instructions= "You are a helpful assistant. Answer the user's questions to the best of your ability.",
    model=model,
    tools = [get_weather, get_location],
    # model_settings= 
    

)