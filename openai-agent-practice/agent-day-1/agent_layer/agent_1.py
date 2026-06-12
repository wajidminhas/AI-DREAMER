from agents import Agent
from configuration_layer.config_1 import gemini_model, groq_model
from tools_layer.tools_1 import check_price, search_product



# agent = Agent(name="Hello Agent", 
#               model=gemini_model, 
#               instructions="You are a helpful assistant that greets the user.")


shopping_agent = Agent(
    name="Shopping Agent",
    model=groq_model,
    instructions="""
    You are a smart shopping assistant.
    - Always search for products first
    - Then check prices
    - Recommend best option based on budget
    - Be concise and helpful
    """,
    tools=[search_product, check_price],
    input_guardrails=["block_bad_words"]
)