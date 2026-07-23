

"""
Response schemas — define what the API returns to users.

Why separate from requests?
- Clear contracts: frontend knows exactly what to expect
- Versioning: can change response format without breaking request format
- Testing: can assert on response structure
"""

from pydantic import BaseModel, Field


class ChatResponse(BaseModel):
    """Agent response returned from the chat endpoint."""
    
    response: str = Field(
        ...,
        description="The agent's text response",
    )
    agent_used: str = Field(
        ...,
        description="Which agent handled the request (for debugging)",
        examples=["Shopping_Agent", "Support_Agent", "Billing_Agent"],
    )