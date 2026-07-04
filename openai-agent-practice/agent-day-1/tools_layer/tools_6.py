


"""
Day 6 — Tools (async versions)

Why async tools now?
Up to Day 5 your tools used the sync `httpx.Client()`. That's fine for a single
agent run, but the moment you want to stream output OR run multiple agent
calls concurrently (this file's whole point), sync I/O inside a tool will
block the event loop and kill your concurrency gains.

@function_tool works with both sync and async functions — just define the
tool as `async def` and use httpx.AsyncClient(). No other change needed.

Groq constraint reminder (still applies here):
- no default values in the signature (`city: str = "Lahore"` breaks Groq)
- simple param types only (str/int/float/bool)
"""

import httpx
from agents import function_tool


@function_tool
async def search_products(query: str) -> str:
    """Search products from an external API by keyword."""
    limit = 5  # default lives in the body, not the signature (Groq rule)
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://dummyjson.com/products/search",
            params={"q": query, "limit": limit},
        )
        r.raise_for_status()
        products = r.json().get("products", [])

    if not products:
        return f"No products found for '{query}'."

    return "\n".join(
        f"ID:{p['id']} | {p['title']} | ${p['price']} | Rating:{p['rating']}"
        for p in products
    )


@function_tool
async def get_weather(city: str) -> str:
    """Get the current weather summary for a city."""
    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://wttr.in/{city}", params={"format": "3"})
        r.raise_for_status()
    return r.text.strip()