

"""
Day 6 — Streaming + Async Patterns

Two separate concepts bundled into one day, both important for a backend
dev's mental model:

1. STREAMING (`Runner.run_streamed`)
   Instead of awaiting one final result, you get an async iterator of
   events as the agent works. Three event types matter in practice:

     - "raw_response_event"        -> raw token deltas from the LLM
                                       (this is what makes a UI feel "live")
     - "run_item_stream_event"     -> higher-level items: tool_call_item,
                                       tool_call_output_item, message_output_item
     - "agent_updated_stream_event"-> fires when a handoff switches agents

2. ASYNC CONCURRENCY (`asyncio.gather`)
   This has nothing to do with streaming. It's about not awaiting agent
   calls one-by-one when they're independent. `Runner.run` is already a
   coroutine, so N independent queries can run concurrently instead of
   N * latency sequentially.

   This is the same reasoning you'd apply to any I/O-bound backend
   workload (concurrent DB calls, concurrent HTTP calls) -- an LLM call
   is just another I/O-bound call.

Groq note: streaming works the same way through OpenAIChatCompletionsModel
as it does for OpenAI's own models, since it's all going through the
Chat Completions streaming protocol under the hood. Tool-call argument
deltas can arrive in one chunk on Groq rather than token-by-token -- don't
be surprised if tool_call_item shows up as a single event instead of a
gradual stream.
"""

import asyncio

from agents import Runner
from agent_layer.agent_6 import streaming_agent
from context_layer.shopping_day4 import ShoppingContext  # existing Day 4 context dataclass


async def run_streamed(query: str, ctx: ShoppingContext) -> str:
    """
    Streams a single agent run token-by-token to stdout.
    Returns the aggregated final text so callers can log/store it.
    """
    print(f"\n--- streaming run: {query!r} ---")
    result = Runner.run_streamed(streaming_agent, input=query, context=ctx)

    final_text_parts: list[str] = []
    async for event in result.stream_events():
        # 1. Raw token deltas -- the actual text being generated, piece by piece
        if event.type == "raw_response_event" and isinstance(event.data, "delta"):
            delta = event.data.delta
            if isinstance(delta, str):
                print(delta, end="", flush=True)
                final_text_parts.append(delta)

        # 2. Higher-level items -- tool calls and their outputs
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                tool_name = getattr(event.item.raw_item, "name", "unknown_tool")
                print(f"\n[tool call] {tool_name}")
            elif event.item.type == "tool_call_output_item":
                print(f"[tool result] {event.item.output}")

        # 3. Handoff notifications -- relevant once you reintroduce handoffs
        elif event.type == "agent_updated_stream_event":
            print(f"\n[handed off to] {event.new_agent.name}")

    print()  # newline once the stream ends
    return "".join(final_text_parts)


async def run_concurrent(queries: list[str], ctx: ShoppingContext) -> list[str]:
    """
    Fires off multiple independent agent runs concurrently instead of
    awaiting them one at a time. Use this for batch jobs, fan-out
    processing, or serving several users' requests in the same beat.

    NOTE: all concurrent runs share the same `ctx` object here for
    simplicity. In a real multi-user backend, build a separate context
    per user/request instead of sharing one.
    """
    tasks = [Runner.run(streaming_agent, input=q, context=ctx) for q in queries]
    results = await asyncio.gather(*tasks)
    return [r.final_output for r in results]


async def run_pipeline():
    ctx = ShoppingContext(user_id="u1", user_name="Ahmad")

    # Pattern 1: single streamed run -- good for live chat UX
    await run_streamed("Find me wireless earbuds under $50", ctx)

    # Pattern 2: concurrent batch -- good for background jobs / multi-user load
    print("\n--- concurrent batch run ---")
    labels = ["weather Lahore", "gaming laptops", "weather Karachi"]
    queries = [
        "What's the weather in Lahore?",
        "Search for gaming laptops",
        "What's the weather in Karachi?",
    ]
    answers = await run_concurrent(queries, ctx)

    for label, answer in zip(labels, answers):
        print(f"\n> {label}\n{answer}")