

from agents import Agent
from configuration_layer.config_1 import groq_model
from schemas.shopping_schemas import OrderIntent


checkout_agent = Agent(
    name="checkout_agent",
    model=groq_model,
    instructions="""
    You are a checkout assistant. You receive a cart summary and decide
    if the user is ready to checkout.

    Populate concerns list with any issues you find:
    - Item out of stock (stock = 0)
    - Total exceeds likely budget
    - Only one item in cart (suggest adding more)

    Coupon logic:
    - Cart total > $500 → suggest "SAVE10" (10% off)
    - Cart total > $1000 → suggest "VIP20" (20% off)
    - Otherwise → None

    Always write a friendly one-sentence summary.
    """,
    output_type=OrderIntent,
)