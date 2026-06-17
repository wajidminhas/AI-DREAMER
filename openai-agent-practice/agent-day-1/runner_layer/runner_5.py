
from context_layer.shopping_day4 import ShoppingContext
from agent_layer.agent_5 import context_agent
from agents import Runner

async def run_with_context(user_id : str, user_name : str, tier : str = "regular"):
    ctx = ShoppingContext(
        user_id=user_id,
        user_name=user_name,
        tier=tier
    )
    
    user_input = "Can you recommend me a phone?"
    
    print(f"\n Running context-aware agent for {user_name} with tier {tier} and user_id {user_id}\n")
    result = await Runner.run(
        starting_agent=context_agent,
        input=user_input,
        context=ctx
    )
    
    print(f"Agent: {result.final_output}\n")

    # ctx is mutated during the run — inspect it after
    print("--- Context After Run ---")
    print(f"User     : {ctx.user_name} ({ctx.tier})")
    print(f"Actions  : {ctx.actions_taken}")
    print(f"Last query: {ctx.last_query}")