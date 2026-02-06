"""
API with JSON Validation using Pydantic - Complete Solution
Validate JSON input using Pydantic before processing
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
import json

print("="*50)
print("PYDANTIC BASICS")
print("="*50)

class SimpleProduct(BaseModel):
    """A simple product model for validation."""
    name: str
    price: float
    quantity: int = 1  # Default value
    
    @validator('price')
    def price_must_be_positive(cls, v):
        """Validate that price is positive."""
        if v <= 0:
            raise ValueError('Price must be positive')
        return v
    
    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        """Validate that quantity is positive."""
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v

# Test validation
print("\n1. Valid data:")
try:
    product1 = SimpleProduct(name="Widget", price=10.99, quantity=5)
    print(f"  ✓ Valid: {product1.name} - ${product1.price}")
except Exception as e:
    print(f"  ✗ Error: {e}")

print("\n2. Invalid data (negative price):")
try:
    product2 = SimpleProduct(name="Widget", price=-10.99)
except Exception as e:
    print(f"  ✗ Validation error (expected): {e}")

print("\n✓ Pydantic basics working!")

from pydantic import BaseModel, Field, validator
from typing import List, Literal


class ProductListing(BaseModel):
    title: str = Field(..., min_length=5, max_length=120)
    category: str = Field(..., min_length=2, max_length=40)
    condition: Literal["new", "used", "refurbished", "unknown"]
    key_features: List[str] = Field(..., min_items=3, max_items=10)
    description: str = Field(..., min_length=40, max_length=2000)

    @validator("title")
    def title_no_json_noise(cls, v: str) -> str:
        v = v.strip()
        if v.startswith("{") or v.endswith("}"):
            raise ValueError("Title looks like JSON/noisy output.")
        return v

    @validator("category")
    def category_clean(cls, v: str) -> str:
        v = v.strip()
        if len(v.split()) > 4:
            raise ValueError("Category should be short (max 4 words).")
        return v

    @validator("key_features", each_item=True)
    def features_quality(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 6:
            raise ValueError("Each key feature must be at least 6 characters.")
        if v.endswith("."):
            raise ValueError("Key features should not end with a period.")
        return v

    @validator("description")
    def description_not_bullets_only(cls, v: str) -> str:
        v = v.strip()
        lines = [ln.strip() for ln in v.splitlines() if ln.strip()]
        if len(lines) >= 3 and all(ln.startswith(("-", "•")) for ln in lines):
            raise ValueError("Description should be a paragraph, not only bullet points.")
        return v


class ProductListingRecord(BaseModel):
    image_path: str = Field(..., min_length=5)
    listing: ProductListing

# Test validation with realistic data
if __name__ == "__main__":
    # ✅ VALID
    ok = ProductListingRecord(
        image_path="/path/to/img.jpg",
        listing={
            "title": "Blue Sport T-Shirt",
            "category": "Fashion",
            "condition": "new",
            "key_features": [
                "Regular fit, comfortable",
                "Breathable fabric feel",
                "Sporty casual style"
            ],
            "description": "A sporty blue t-shirt with a clean, casual look. Great for everyday wear and light activities."
        }
    )
    print("✓ Valid record:", ok.model_dump())

    # ❌ INVALID (condition sbagliata)
    try:
        ProductListing(condition="brand_new", title="X", category="Fashion", key_features=["ok ok ok"], description="desc"*20)
    except Exception as e:
        print("✓ Invalid blocked (expected):", e)