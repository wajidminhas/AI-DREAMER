
from agents import Agent
from configuration_layer.config_1 import gemini_model




context_aware_agent = Agent(
    name="Context_Aware_Agent",
    model=gemini_model,
    instructions="""
    You are a smart shopping assistant.
    - Always search for products first
    - Then check prices
    - Recommend best option based on budget
    - Be concise and helpful
    """,
    # tools=[search_product, check_price],
    # input_guardrails=["block_bad_words"],
    
)