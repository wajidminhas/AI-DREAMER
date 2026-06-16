


from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class CartItem:
    product_id: str
    name: str
    price: float
    quantity: int


@dataclass
class ShoppingContext:
    # Identity
    user_id: str
    user_name: str
    tier: str = "regular"           # "regular" | "premium" | "vip"

    # Session state
    cart: list[CartItem] = field(default_factory=list)
    applied_coupon: Optional[str] = None
    session_start: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    # Routing metadata
    current_agent: str = "triage"
    handoff_reason: Optional[str] = None

    # Billing/support flags
    has_open_ticket: bool = False
    failed_payment_count: int = 0

    # Audit trail
    actions_taken: list[str] = field(default_factory=list)
    last_query: Optional[str] = None