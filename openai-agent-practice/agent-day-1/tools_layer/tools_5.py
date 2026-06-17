


import httpx
from agents import function_tool


BASE_URL = "https://dummyjson.com"


@function_tool
def search_products(query: str, limit: int = 5) -> str:
    """Search for products by keyword using real product API."""
    with httpx.Client() as client:
        response = client.get(
            f"{BASE_URL}/products/search",
            params={"q": query, "limit": limit},
        )
        response.raise_for_status()
        data = response.json()

    products = data.get("products", [])
    if not products:
        return f"No products found for '{query}'"

    results = []
    for p in products:
        results.append(
            f"ID: {p['id']} | {p['title']} | "
            f"${p['price']} | Rating: {p['rating']} | "
            f"Stock: {p['stock']} units | Category: {p['category']}"
        )

    return "\n".join(results)


@function_tool
def get_product_detail(product_id: int) -> str:
    """Get full details of a specific product by ID."""
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/products/{product_id}")
        response.raise_for_status()
        p = response.json()

    return (
        f"Name: {p['title']}\n"
        f"Price: ${p['price']}\n"
        f"Description: {p['description']}\n"
        f"Rating: {p['rating']}\n"
        f"Stock: {p['stock']}\n"
        f"Brand: {p.get('brand', 'N/A')}\n"
        f"Category: {p['category']}"
    )


@function_tool
def get_products_by_category(category: str, limit: int = 5) -> str:
    """Browse products by category."""
    with httpx.Client() as client:
        response = client.get(
            f"{BASE_URL}/products/category/{category}",
            params={"limit": limit},
        )
        response.raise_for_status()
        data = response.json()

    products = data.get("products", [])
    if not products:
        return f"No products in category '{category}'"

    results = []
    for p in products:
        results.append(
            f"ID: {p['id']} | {p['title']} | ${p['price']} | Stock: {p['stock']}"
        )

    return "\n".join(results)