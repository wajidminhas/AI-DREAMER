


from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ShoppingContext:
    user_id : str
    user_name : str
    cart :list[str] = field(default_factory= list)
    last_query : Optional[str] = None
    total_interactions : int = 0