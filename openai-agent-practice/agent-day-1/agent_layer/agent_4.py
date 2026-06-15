


from agents import Agent
from configuration_layer.config_1 import gemini_model



memory_agent = Agent(
    name = "memory_agent",
    model = gemini_model,
    instructions = """
    You are a helpful shopping assistant with memory.
    You remember everything the user has told you in this conversation.
    """,
)

