

"""
Day 6 — Streaming-capable agent

No new agent concepts here — it's the same Agent() shape as Day 5's doer
agent. Streaming is a property of how you call Runner, not how you define
the Agent. This agent just has async tools so it plays nicely with
concurrent runs.

Swap the import below for wherever your MODEL instance actually lives
(configuration_layer/config.py from Day 1).
"""

from agents import Agent
from configuration_layer.config_1 import groq_model, gemini_model
from tools_layer.tools_6 import search_products, get_weather

streaming_agent = Agent(
    name="streaming_agent",
    model=groq_model,
    instructions=(
        "You are a helpful assistant with access to product search and "
        "weather tools. Use a tool whenever the user's question needs "
        "live data. Keep replies concise."
    ),
    tools=[search_products, get_weather],
)