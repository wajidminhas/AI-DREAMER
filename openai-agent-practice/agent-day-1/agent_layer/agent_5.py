from agents import Agent
from configuration_layer.config_1 import gemini_model
from tools_layer.tools_4 import remember_preference, recall_preferences



context_agent = Agent(
    name="context_agent",
    model=gemini_model,
    instructions="""
    You are a personalized shopping assistant.
    The user's name, tier, and cart are available in your context.
    Use remember_preference to save things the user likes.
    Use recall_preferences to check saved preferences before recommending.
    Always address the user by name.
    """,
    tools=[remember_preference, recall_preferences],
)