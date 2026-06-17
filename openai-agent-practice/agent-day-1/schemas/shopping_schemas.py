

from pydantic import BaseModel, Field
from typing import Optional


class ProductRecommendation(BaseModel):
    product_id: str
    name: str
    price: float
    currency: str = "USD"
    recommendation_score: float = Field(ge=0.0, le=1.0)
    reason: str
    in_stock: bool


class SearchResult(BaseModel):
    query_understood: str
    recommendations: list[ProductRecommendation]
    follow_up_question: Optional[str] = None


class OrderIntent(BaseModel):
    ready_to_checkout: bool
    cart_total: float
    concerns: list[str]
    suggested_coupon: Optional[str] = None
    summary: str