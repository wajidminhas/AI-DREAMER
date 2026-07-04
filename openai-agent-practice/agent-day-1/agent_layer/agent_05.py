


from agents import Agent
from configuration_layer.config_1 import groq_model

from schemas.shopping_schemas import SearchResult
from tools_layer.tools_5 import search_products, get_product_detail


search_agent = Agent(
    name="search_agent",
    model=groq_model,
    instructions="""
    You are a product search agent with access to a real product database.

    When given a user query:
    1. Call search_products with relevant keywords
    2. Call get_product_detail on the top 2-3 results for deeper info
    3. Return structured recommendations

    Scoring guide for recommendation_score:
    - 0.9-1.0 = perfect match (right category, within budget, high rating)
    - 0.7-0.9 = good match (most criteria met)
    - 0.5-0.7 = partial match (some criteria missing)
    - below 0.5 = poor match (include only if nothing better found)

    If budget is mentioned, exclude products over budget.
    If you need more info, set follow_up_question.
    Always populate all fields in your response.
    """,
    tools=[search_products, get_product_detail]
)


formatter_agent = Agent(
    name="formatter_agent",
    model=groq_model,
    instructions="""
    You receive raw product search results as plain text.
    Your job is to structure them into a clean typed response.

    Scoring guide for recommendation_score:
    - 0.9-1.0 = perfect match
    - 0.7-0.9 = good match
    - 0.5-0.7 = partial match
    - below 0.5 = poor match

    Always populate all fields. Use product ID from the raw text.
    If budget was mentioned and no product fits, set follow_up_question.
    """,
    # NO tools here
    output_type=SearchResult,
)