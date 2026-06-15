
from context_layer.shopping_context import ShoppingContext
from agent_layer.agent_5 import context_aware_agent
from agents import Runner

async def run_with_context():
    ctx = ShoppingContext(
        user_id="123", 
        user_name="John Doe",
        cart=["laptop", "headphones"],)
    
    result = await Runner.run(
        starting_agent=context_aware_agent,
        input=f"what should I buy next? my cart has {ctx.cart}",
        context=ctx
    )
    
    print(result.final_output)
    print(f"Context after run: {ctx}")