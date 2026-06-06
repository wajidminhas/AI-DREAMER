


from agents import Agent, handoff
from pydantic import BaseModel
from configuration_layer.config_1 import gemini_model
from tools_layer.tools_1 import search_product, check_price

# from tool_layer.tools_1 import search_product, check_price


class AgentSchemas(BaseModel):
    pass

# ✅ Agent 1 — Shopping Specialist
shopping_agent = Agent(
    name="Shopping_Agent",
    model=gemini_model,
    instructions="""
    You are a specialist shopping assistant.
    - Search for products when user asks
    - Always check prices after finding products
    - Recommend best option based on budget
    - Be concise and helpful
    """,
    tools=[search_product, check_price]
)

# ✅ Agent 2 — Support Specialist
support_agent = Agent(
    name="Support_Agent",
    model=gemini_model,
    instructions="""
    You are a customer support specialist.
    - Handle complaints professionally
    - Always apologize for inconvenience
    - Provide clear solutions
    - Be empathetic and helpful
    """,
)

# ✅ Agent 3 — Billing Specialist
billing_agent = Agent(
    name="Billing_Agent",
    model=gemini_model,
    instructions="""
    You are a billing specialist.
    - Handle payment queries
    - Explain charges clearly
    - Process refund requests
    - Be transparent and helpful
    """,
)

# ✅ Triage Agent — The Orchestrator
triage_agent = Agent(
    name="Triage_Agent",
    model=gemini_model,
    instructions="""
    You are a smart triage assistant.
    Analyze user intent and route to right specialist:
    - Shopping queries    → Shopping Agent
    - Complaints/issues   → Support Agent
    - Payment/billing     → Billing Agent
    Always handoff — never answer directly yourself.
    """,
    handoffs=[handoff(shopping_agent), handoff(support_agent), handoff(billing_agent)]
)