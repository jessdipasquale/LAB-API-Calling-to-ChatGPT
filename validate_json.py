import json
from pathlib import Path
from typing import List, Tuple

from product_listing_project.models import ProductListingRecord


def load_and_validate_records(json_path: str) -> Tuple[List[dict], List[dict]]:
    """
    Loads a JSON file containing a list of ProductListingRecord objects
    and validates each entry with Pydantic.

    Returns:
      - validated_records: list of validated dicts
      - errors: list of error dicts with index + details
    """
    path = Path(json_path)

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("JSON root must be a list of records.")

    validated_records = []
    errors = []

    for i, item in enumerate(data):
        try:
            record = ProductListingRecord(**item)
            validated_records.append(record.model_dump())
        except Exception as e:
            errors.append({
                "index": i,
                "error": str(e)
            })

    return validated_records, errors


if __name__ == "__main__":
    # Test with valid JSON
    valid_data, valid_errors = load_and_validate_records("sample_valid.json")
    print("\n=== VALID FILE RESULTS ===")
    print("Validated:", len(valid_data))
    print("Errors:", len(valid_errors))
    if valid_errors:
        print(valid_errors[0])

    # Test with invalid JSON
    invalid_data, invalid_errors = load_and_validate_records("sample_invalid.json")
    print("\n=== INVALID FILE RESULTS ===")
    print("Validated:", len(invalid_data))
    print("Errors:", len(invalid_errors))
    if invalid_errors:
        print("First error:\n", invalid_errors[0]["error"])