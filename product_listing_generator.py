from datasets import load_dataset
import requests
from PIL import Image
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()

print(os.getenv("OPENAI_API_KEY"))

import os

print(os.getenv("OPENAI_API_KEY") is not None)

from datasets import load_dataset
import requests
from PIL import Image
import pandas as pd
from pathlib import Path

print("Loading product dataset...")
try:
    dataset = load_dataset("ashraq/fashion-product-images-small", split="train[:100]")  # First 100 samples
    print(f"✓ Loaded {len(dataset)} products")

    products_df = pd.DataFrame(dataset)
    print(f"Dataset columns: {products_df.columns.tolist()}")

except Exception as e:
    print(f"⚠ Could not load HuggingFace dataset: {e}")
    print("Using local images instead...")

    
    
    products_data = [
        {
            "id": 1,
            "name": "Blue Sport T-Shirt",
            "price": 79.99,
            "category": "Fashion",
            "image_path": "images/product1.jpg"
        },
        {
            "id": 2,
            "name": "Red Casual Dress",
            "price": 129.99,
            "category": "Fashion",
            "image_path": "images/product2.jpg"
        },
        {
            "id": 3,
            "name": "Green Running Shoes",
            "price": 89.99,
            "category": "Fashion",
            "image_path": "images/product3.jpg"
        }
    ]

    products_df = pd.DataFrame(products_data)

from pathlib import Path

base_dir = Path.home() / "Desktop" / "Ironhack" / "Week1" / "20260205" / "product_listing_project" / "product_images"

assert base_dir.exists(), f"❌ Folder not found: {base_dir}"

IMAGE_PATHS = sorted([
    str(p) for p in base_dir.iterdir()
    if p.suffix.lower() in [".jpg", ".jpeg", ".png"]
])

assert len(IMAGE_PATHS) >= 1, f"❌ No images found in: {base_dir}"

print("✅ Images found:", len(IMAGE_PATHS))
print("First image:", IMAGE_PATHS[0])

print(f"\n✓ Dataset prepared!")
print(f"  Total products: {len(products_df)}")

#Step 3
import base64
from io import BytesIO

def encode_image_to_base64(pil_image):
    buffer = BytesIO()
    pil_image.save(buffer, format="JPEG")
    img_bytes = buffer.getvalue()
    encoded = base64.b64encode(img_bytes).decode("utf-8")
    return encoded

sample = dataset[0]
image = sample["image"]

encoded_image = encode_image_to_base64(image)

print("Base64 encoding successful!")
print("Encoded string length:", len(encoded_image))
print("Preview:", encoded_image[:100], "...")

#Step 4

def create_product_listing_prompt(product_name, price, category, additional_info=None):
    prompt = f"""You are an expert fashion e-commerce copywriter. Analyze the product image and create a compelling product listing suitable for an online fashion store.

Product Information:
- Name: {product_name}
- Price: ${price:.2f}
- Category: {category}
{f'- Additional Info: {additional_info}' if additional_info else ''}

Please generate a professional fashion product listing that includes:

1. **Product Title**
   - Catchy and SEO-friendly
   - Maximum 60 characters

2. **Product Description** (150-200 words)
   - Describe the style, fit, and overall appearance
   - Mention visible colors, patterns, and materials
   - Explain how and when the item can be worn (casual, formal, seasonal)
   - Use engaging and persuasive language appropriate for fashion e-commerce

3. **Key Features** (5-7 bullet points)
   - Fabric or material
   - Fit or cut
   - Design details visible in the image
   - Comfort and wearability
   - Suitable occasions or seasons

4. **SEO Keywords**
   - 10–15 relevant fashion-related keywords
   - Comma-separated

Format your response strictly as JSON using the following structure:
{{
    "title": "Product title here",
    "description": "Full description here",
    "features": ["Feature 1", "Feature 2", "..."],
    "keywords": "keyword1, keyword2, ..."
}}

Base your description only on what is visible in the image. Do not assume features that are not clearly shown."""

    return prompt

test_prompt = create_product_listing_prompt(
    product_name="Blue sport t-shirt",
    price=79.99,
    category="Fashion",
    additional_info="Available in different colors and sizes."
)

print("\n" + "="*50)
print("PROMPT TEMPLATE")
print("="*50)
print(test_prompt[:500] + "...") 

from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI()

#Step 5

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Hello!"
)

print("Status: received response")
print("Raw text:\n", response.output_text)

import os, json, base64
from openai import OpenAI

client = OpenAI()

def image_to_data_url(image_path):
    ext = os.path.splitext(image_path)[1].lower().replace(".", "")
    mime = "jpeg" if ext in ["jpg", "jpeg"] else ext
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/{mime};base64,{b64}"

img_path = IMAGE_PATHS[0]
img_url = image_to_data_url(img_path)

response = client.responses.create(
    model="gpt-4.1-mini",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": (
                "Return ONLY valid JSON (no extra text). "
                "Create a product listing with fields: "
                "title, category, condition, key_features (array), description."
            )},
            {"type": "input_image", "image_url": img_url},
        ]
    }],
    text={"format": {"type": "json_object"}}
)

raw = response.output_text
print("✅ Response received")
print("Raw output:\n", raw)

parsed = json.loads(raw)
print("✅ JSON parsed correctly")
print(parsed)

raw = response.output_text
print("LEN:", len(raw))
print("RAW repr:", repr(raw[:300]))  

import json
from openai import OpenAI

client = OpenAI()

schema = {
    "name": "simple_response",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "message": {"type": "string"}
        },
        "required": ["message"]
    }
}

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Say hello",
    text={
        "format": {
            "type": "json_schema",
            "name": "simple_response",
            "schema": schema["schema"]   
        }
    }
)

raw = response.output_text
parsed = json.loads(raw)

print("✅ Response received")
print("✅ JSON parsed correctly")
print(parsed)

#Step 6

import os
import json
import base64
from datetime import datetime
from pathlib import Path

from openai import OpenAI
from pydantic import ValidationError

from models import ListingRequest, ProductListing

client = OpenAI()

base_dir = os.path.expanduser(
    "~/Desktop/ironhack/Week1/20260205/product_listing_project/product_images"
)
assert os.path.exists(base_dir), "❌ The product_images folder does not exist"

IMAGE_PATHS = [
    os.path.join(base_dir, filename)
    for filename in os.listdir(base_dir)
    if filename.lower().endswith((".jpg", ".jpeg", ".png"))
]
assert len(IMAGE_PATHS) >= 1, "❌ No images found"

print("Images found:")
for path in IMAGE_PATHS:
    print(" -", path)

LISTING_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "title": {"type": "string"},
        "category": {"type": "string"},
        "condition": {
            "type": "string",
            "enum": ["new", "used", "refurbished", "unknown"]
        },
        "key_features": {
            "type": "array",
            "items": {"type": "string"}
        },
        "description": {"type": "string"}
    },
    "required": ["title", "category", "condition", "key_features", "description"]
}

def image_to_data_url(image_path: str) -> str:
    extension = os.path.splitext(image_path)[1].lower().replace(".", "")
    mime_type = "jpeg" if extension in ["jpg", "jpeg"] else extension

    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    return f"data:image/{mime_type};base64,{encoded_image}"


def generate_product_listing(valid_request: ListingRequest) -> ProductListing:
    """
    1) Chiamata API
    2) Parse JSON
    3) VALIDAZIONE OUTPUT con Pydantic (ProductListing)
    """
    image_data_url = image_to_data_url(valid_request.image_path)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Create a product listing from this image."},
                {"type": "input_image", "image_url": image_data_url},
                {"type": "input_text", "text": "Return ONLY valid JSON that matches the schema."}
            ]
        }],
        text={
            "format": {
                "type": "json_schema",
                "name": "product_listing",
                "schema": LISTING_SCHEMA
            }
        }
    )

    raw = response.output_text
    data = json.loads(raw)

    return ProductListing.model_validate(data)


results = []
errors = []

for image_path in IMAGE_PATHS:

    try:
        req = ListingRequest(image_path=image_path)
    except ValidationError as e:
        errors.append({
            "image_path": image_path,
            "stage": "input_validation",
            "error": e.errors()
        })
        print(f"❌ Input invalid: {os.path.basename(image_path)}")
        continue  

    try:
        listing = generate_product_listing(req)

        results.append({
            "image_path": image_path,
            "listing": listing.model_dump()
        })
        print(f"✅ Processed: {os.path.basename(image_path)}")

    except ValidationError as e:
        errors.append({
            "image_path": image_path,
            "stage": "output_validation",
            "error": e.errors()
        })
        print(f"❌ Output invalid: {os.path.basename(image_path)}")

    except json.JSONDecodeError as e:
        errors.append({
            "image_path": image_path,
            "stage": "json_parse",
            "error": str(e)
        })
        print(f"❌ JSON parse error: {os.path.basename(image_path)}")

    except Exception as e:
        errors.append({
            "image_path": image_path,
            "stage": "unknown",
            "error": str(e)
        })
        print(f"❌ Unknown error: {os.path.basename(image_path)}")


SCRIPT_DIR = Path(__file__).parent
results_file = SCRIPT_DIR / "product_listings.json"
errors_file = SCRIPT_DIR / "product_listing_errors.json"

with open(results_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

with open(errors_file, "w", encoding="utf-8") as f:
    json.dump(errors, f, indent=2, ensure_ascii=False)

print("\n📦 FINAL SUMMARY")
print("Total products processed:", len(IMAGE_PATHS))
print("Successful listings:", len(results))
print("Errors:", len(errors))
print("Saved files:")
print(" -", results_file)
print(" -", errors_file)