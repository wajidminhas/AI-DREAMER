
from agents import function_tool


@function_tool
async def get_weather(city: str) -> str:
    # Simulate a weather API call
    return f"The weather in {city} is sunny with a high of 25°C."