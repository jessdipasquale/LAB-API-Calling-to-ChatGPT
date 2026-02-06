from pydantic import BaseModel, Field
from typing import List, Literal, Optional

Condition = Literal["new", "used", "refurbished", "unknown"]

class ListingRequest(BaseModel):
    """
    INPUT validation (prima della chiamata API)
    """
    image_path: str = Field(..., min_length=1)

    # opzionali (se vuoi usarli nel prompt in futuro)
    product_name: Optional[str] = None
    price: Optional[float] = Field(default=None, ge=0)
    category_hint: Optional[str] = None


class ProductListing(BaseModel):
    """
    OUTPUT validation (dopo la chiamata API)
    """
    title: str = Field(..., min_length=1, max_length=80)
    category: str = Field(..., min_length=1)
    condition: Condition
    key_features: List[str] = Field(..., min_length=1, max_length=12)
    description: str = Field(..., min_length=1)