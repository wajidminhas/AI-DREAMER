
"""
Request schemas — validate what users send to the API.

Why Pydantic schemas?
- Automatic validation: FastAPI rejects bad input before it reaches your code
- Documentation: generates OpenAPI docs automatically
- Type safety: IDE knows what fields exist
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """User message sent to the chat endpoint."""
    
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The user's message to the agent",
        examples=["I want to buy a laptop under $500"],
    )
    user_id: str = Field(
        default="anonymous",
        description="Optional user identifier for personalization",
    )
    session_id: str | None = Field(
        default=None,
        description="Optional session ID for multi-turn conversations",
    )