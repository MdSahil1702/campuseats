"""assignment6-errors/validation.py
C1: JSON Schema for POST /orders body.
C2: validate() collects ALL errors (not just first); returns (ok, errors).
"""

ORDER_SCHEMA = {
    "type": "object",
    "required": ["customer", "items", "address"],
    "properties": {
        "customer": {"type": "string", "minLength": 1},
        "items": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["id", "qty"],
                "properties": {
                    "id":  {"type": "string", "minLength": 1},
                    "qty": {"type": "integer", "minimum": 1},
                },
            },
        },
        "address": {"type": "string", "minLength": 1},
    },
}


def _validate_items(items, errors):
    if not isinstance(items, list):
        errors.append({"field": "items", "reason": "must be an array"})
        return
    if len(items) == 0:
        errors.append({"field": "items", "reason": "must contain at least one item"})
        return
    for i, it in enumerate(items):
        if not isinstance(it, dict):
            errors.append({"field": f"items[{i}]", "reason": "must be an object"})
            continue
        if "id" not in it or not isinstance(it["id"], str) or not it["id"]:
            errors.append({"field": f"items[{i}].id", "reason": "required, non-empty string"})
        if "qty" not in it:
            errors.append({"field": f"items[{i}].qty", "reason": "required"})
        else:
            q = it["qty"]
            if not isinstance(q, int) or isinstance(q, bool):
                errors.append({"field": f"items[{i}].qty", "reason": "must be an integer"})
            elif q < 1:
                errors.append({"field": f"items[{i}].qty", "reason": "must be >= 1"})


def validate(payload):
    """Return (ok: bool, errors: list[dict]). Collects ALL errors."""
    errors = []
    if not isinstance(payload, dict):
        return False, [{"field": "body", "reason": "must be a JSON object"}]

    if "customer" not in payload:
        errors.append({"field": "customer", "reason": "required"})
    elif not isinstance(payload["customer"], str) or not payload["customer"]:
        errors.append({"field": "customer", "reason": "must be a non-empty string"})

    if "address" not in payload:
        errors.append({"field": "address", "reason": "required"})
    elif not isinstance(payload["address"], str) or not payload["address"]:
        errors.append({"field": "address", "reason": "must be a non-empty string"})

    if "items" not in payload:
        errors.append({"field": "items", "reason": "required"})
    else:
        _validate_items(payload["items"], errors)

    return (len(errors) == 0), errors
