"""assignment6-errors/problem.py
RFC 7807 Problem Details for all errors.
Single shape: type / title / status / detail / errors[]
Content-Type: application/problem+json
"""
import json
from http.server import BaseHTTPRequestHandler

# ---------- B2: stable type catalogue ----------
TYPE_BASE = "https://campuseats.example.com/problems/"

TYPES = {
    "empty-cart":         TYPE_BASE + "empty-cart",
    "item-unavailable":   TYPE_BASE + "item-unavailable",
    "payment-declined":   TYPE_BASE + "payment-declined",
    "order-not-found":    TYPE_BASE + "order-not-found",
    "illegal-transition": TYPE_BASE + "illegal-transition",
    "validation-failed":  TYPE_BASE + "validation-failed",
    "malformed-json":     TYPE_BASE + "malformed-json",
    "unauthorized":       TYPE_BASE + "unauthorized",
    "not-acceptable":     TYPE_BASE + "not-acceptable",
    "rate-limited":       TYPE_BASE + "rate-limited",
    "internal-error":     TYPE_BASE + "internal-error",
}

TITLES = {
    "empty-cart":         "Empty Cart",
    "item-unavailable":   "Item Unavailable",
    "payment-declined":   "Payment Declined",
    "order-not-found":    "Order Not Found",
    "illegal-transition": "Illegal State Transition",
    "validation-failed":  "Validation Failed",
    "malformed-json":     "Malformed JSON",
    "unauthorized":       "Unauthorized",
    "not-acceptable":     "Not Acceptable",
    "rate-limited":       "Too Many Requests",
    "internal-error":     "Internal Server Error",
}

STATUSES = {
    "empty-cart":         422,
    "item-unavailable":   409,
    "payment-declined":   402,
    "order-not-found":    404,
    "illegal-transition": 409,
    "validation-failed":  422,
    "malformed-json":     400,
    "unauthorized":       401,
    "not-acceptable":     406,
    "rate-limited":       429,
    "internal-error":     500,
}


def problem_body(kind, detail="", errors=None, extra=None):
    """Build the RFC 7807 Problem Details body."""
    body = {
        "type":   TYPES.get(kind, TYPE_BASE + kind),
        "title":  TITLES.get(kind, kind.replace("-", " ").title()),
        "status": STATUSES.get(kind, 500),
        "detail": detail,
    }
    if errors:
        body["errors"] = errors
    if extra:
        body.update(extra)
    return body


def send_problem(handler: BaseHTTPRequestHandler, kind, detail="",
                 errors=None, extra=None, headers=None):
    """B1: Every failure goes through this — one shape, one Content-Type."""
    body = problem_body(kind, detail, errors, extra)
    data = json.dumps(body).encode("utf-8")
    handler.send_response(body["status"])
    handler.send_header("Content-Type", "application/problem+json; charset=utf-8")
    handler.send_header("Content-Length", str(len(data)))
    handler.send_header("Cache-Control", "no-store")
    if headers:
        for k, v in headers.items():
            handler.send_header(k, v)
    handler.end_headers()
    handler.wfile.write(data)
