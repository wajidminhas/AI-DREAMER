
# from agents import Runner

# # from runner_layer.runner_1 import result
# from agent_layer.agent_1 import shopping_agent

# res = Runner.run_sync(
#     starting_agent=shopping_agent,
#     input="Find me a laptop and check its price"
# )

# print("Final Result:", res.final_output)

# ----------------------------- Multiple Agents with Triage -----------------------------

import time

from agent_layer.agent_2 import triage_agent, support_agent, billing_agent, shopping_agent
from agent_layer.agent_3 import block_bad_words
from agents import InputGuardrailTripwireTriggered, Runner
import asyncio
from runner_layer.runner_4 import run_conversation
from runner_layer.runner_5 import run_with_context

print("🤖 Multi-Agent System Starting...\n")

# Test 1 — Shopping query
# result = Runner.run_sync(
#     starting_agent=triage_agent,
#     input="Find me a laptop under $500"
# )
# print("Test 1 - Shopping:")
# print(result.final_output)
# print("\n" + "="*50 + "\n")

# time.sleep(30)  # Just to separate the outputs clearly

# # Test 2 — Support query
# result = Runner.run_sync(
#     starting_agent=triage_agent,
#     input="My order arrived damaged, I want to complain"
# )
# print("Test 2 - Support:")
# print(result.final_output)
# print("\n" + "="*50 + "\n")


# time.sleep(30)  # Just to separate the outputs clearly

# # Test 3 — Billing query
# result = Runner.run_sync(
#     starting_agent=triage_agent,
#     input="I was charged twice for my order"
# )
# print("Test 3 - Billing:")
# print(result.final_output)


# try:
#     result = Runner.run_sync(
#         starting_agent=shopping_agent,
#         input="Find me a laptop under $500"
#     )
#     print(result.final_output)
# except InputGuardrailTripwireTriggered:
#     print("🛑 Blocked! This message was not allowed.")




if __name__ == "__main__":
    asyncio.run(run_with_context(
        user_id="user_001",
        user_name="Ahmad",
        tier="vip",
    ))