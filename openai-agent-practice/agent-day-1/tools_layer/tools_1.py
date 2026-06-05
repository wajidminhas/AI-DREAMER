



from agents import function_tool

# ✅ Tool 1 — Product Search
@function_tool
def search_product(query: str) -> str:
    """Search for a product by name or category"""
    
    products = {
        "laptop": "Dell Inspiron 15, HP Pavilion, Lenovo IdeaPad",
        "phone": "Samsung Galaxy S24, Pixel 8, iPhone 15",
        "jacket": "Nike Winter Parka, Adidas Puffer, Zara Wool Coat",
    }
    
    for key in products:
        if key in query.lower():
            return f"Found products: {products[key]}"
    
    return "No products found for your query"


# ✅ Tool 2 — Price Checker
@function_tool
def check_price(product_name: str) -> str:
    """Check price of a specific product"""
    
    prices = {
        "dell inspiron 15": "$450",
        "hp pavilion": "$480",
        "lenovo ideapad": "$399",
        "samsung galaxy s24": "$799",
        "nike winter parka": "$89",
    }
    
    for key in prices:
        if key in product_name.lower():
            return f"Price of {product_name}: {prices[key]}"
    
    return f"Price not found for {product_name}"