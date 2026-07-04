


from agents import Runner
from agent_layer.agent_05 import search_agent, formatter_agent
from agent_layer.agent_005 import checkout_agent

from context_layer.shopping_day4 import ShoppingContext
from schemas.shopping_schemas import SearchResult, OrderIntent



async def run_search(user_query: str, ctx: ShoppingContext) -> SearchResult:
    # Step 1 — search
    print(f"[Search Agent] Searching for: {user_query}")    
    
    
    raw_result = await Runner.run(
        search_agent,
        input=user_query,
        context=ctx,
    )
    raw_text = raw_result.final_output
    print(f"\n[Search Agent] Raw results fetched.")

    # Step 2 — format raw text into typed Pydantic model
    print(f"[Formatter Agent] Structuring results...")
    format_result = await Runner.run(
        formatter_agent,
        input=f"User query: {user_query}\n\nRaw search results:\n{raw_text}",
        context=ctx,
    )

    search_result: SearchResult = format_result.final_output

    print(f"\n Query understood: {search_result.query_understood}")
    print(f" Recommendations found: {len(search_result.recommendations)}")
    for rec in search_result.recommendations:
        print(
            f"   • {rec.name} — ${rec.price} "
            f"(score: {rec.recommendation_score:.2f}) — {rec.reason}"
        )

    if search_result.follow_up_question:
        print(f"\n Agent needs: {search_result.follow_up_question}")

    return search_result


async def run_checkout(search_result: SearchResult, ctx: ShoppingContext) -> OrderIntent:
    # filter top recommendations only
    top_picks = [r for r in search_result.recommendations if r.recommendation_score >= 0.7]

    if not top_picks:
        top_picks = search_result.recommendations[:2]

    cart_lines = "\n".join([
        f"- {r.name} | ${r.price} | In stock: {r.in_stock}"
        for r in top_picks
    ])
    cart_total = sum(r.price for r in top_picks)

    checkout_input = (
        f"User: {ctx.user_name} ({ctx.tier} tier)\n"
        f"Cart:\n{cart_lines}\n"
        f"Estimated total: ${cart_total:.2f}"
    )

    print(f"\n[Checkout Agent] Evaluating cart...")

    result = await Runner.run(
        checkout_agent,
        input=checkout_input,
        context=ctx,
    )

    order: OrderIntent = result.final_output

    print(f"\n Ready to checkout: {order.ready_to_checkout}")
    print(f" Cart total: ${order.cart_total:.2f}")
    if order.concerns:
        print(f" Concerns: {order.concerns}")
    if order.suggested_coupon:
        print(f" Suggested coupon: {order.suggested_coupon}")
    print(f" Summary: {order.summary}")

    return order


async def run_day5_pipeline(user_query: str, user_id: str, user_name: str, tier: str = "regular"):
    ctx = ShoppingContext(user_id=user_id, user_name=user_name, tier=tier)

    # Step 1 — search
    search_result = await run_search(user_query, ctx)

    # Step 2 — checkout with typed output from step 1
    order = await run_checkout(search_result, ctx)

    return search_result, order