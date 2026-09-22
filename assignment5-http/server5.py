"""assignment5-http/server5.py
Assignment 5 HTTP server — HTTP Methods & Headers.
Reuses Assignment 4 via `store5.ExtendedStore` (which mirrors A4 semantics).
All A4 behaviour preserved: idempotency key, validation, status codes.
"""
import gzip
import io
import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from store5 import ExtendedStore

STORE = ExtendedStore()

# ---------- A1 METHOD MAP (also used in NOTES.md) ----------
METHOD_MAP = {
    "list_orders":      ("GET",     "/orders"),
    "read_order":       ("GET",     "/orders/{id}"),
    "create_order":     ("POST",    "/orders"),
    "replace_order":    ("PUT",     "/orders/{id}"),
    "modify_order":     ("PATCH",   "/orders/{id}"),
    "delete_order":     ("DELETE",  "/orders/{id}"),
    "cancel_order":     ("POST",    "/orders/{id}/cancellation"),
    "checkout_order":   ("POST",    "/orders/{id}/checkout"),
    "set_availability": ("POST",    "/restaurants/{id}/availability"),
    "options_orders":   ("OPTIONS", "/orders"),
    "receipt_redirect": ("GET",     "/orders/{id}/receipt"),
}

VALID_TOKEN = "campuseats-token"


class Handler(BaseHTTPRequestHandler):
    server_version = "CampusEats/5.0"
    protocol_version = "HTTP/1.1"

    # ---------- low-level send ----------
    def _common_headers(self):
        # B7 security + B6 CORS
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS")
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type, Authorization, Idempotency-Key, If-Match, "
            "If-None-Match, X-HTTP-Method-Override, Accept, Accept-Encoding",
        )
        self.send_header(
            "Access-Control-Expose-Headers",
            "ETag, Location, X-RateLimit-Limit, X-RateLimit-Remaining, Retry-After",
        )

    def _send(self, status, body=None, headers=None):
        self.send_response(status)
        self._common_headers()
        if headers:
            for k, v in headers.items():
                self.send_header(k, v)
        if body is None:
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        data = json.dumps(body).encode()
        # B1 gzip for large JSON
        if len(data) > 256 and "gzip" in self.headers.get("Accept-Encoding", ""):
            buf = io.BytesIO()
            with gzip.GzipFile(fileobj=buf, mode="wb") as f:
                f.write(data)
            data = buf.getvalue()
            self.send_header("Content-Encoding", "gzip")
            self.send_header("Vary", "Accept-Encoding")
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _problem(self, status, title, detail=""):
        self._send(status, {
            "type": "about:blank",
            "title": title,
            "status": status,
            "detail": detail,
        })

    # ---------- B1, B3, B5 ----------
    def _check_accept(self):
        accept = self.headers.get("Accept", "*/*")
        if "application/json" not in accept and "*/*" not in accept:
            self._problem(406, "Not Acceptable",
                          "Only application/json is supported")
            return False
        return True

    def _auth(self):
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer ") or len(auth) <= len("Bearer "):
            self._problem(401, "Unauthorized", "Bearer token required")
            return False
        return True

    def _rate(self):
        client = self.client_address[0]
        allowed, remaining, limit = STORE.check_rate(client, limit=100, window=60)
        if not allowed:
            self._send(429, {"title": "Too Many Requests"},
                       {"X-RateLimit-Limit": str(limit),
                        "X-RateLimit-Remaining": "0",
                        "Retry-After": "60"})
            return False
        self._rate_headers = {
            "X-RateLimit-Limit": str(limit),
            "X-RateLimit-Remaining": str(remaining),
        }
        return True

    def _read_body(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return None
        raw = self.rfile.read(length)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return "__INVALID__"

    # ---------- A5 X-HTTP-Method-Override (documented fallback) ----------
    def _apply_override(self, method):
        ov = self.headers.get("X-HTTP-Method-Override")
        if ov and method == "POST":
            return ov.upper()
        return method

    # ---------- main router ----------
    def _route(self, method):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)
        method = self._apply_override(method)

        if not self._rate():
            return
        if not self._check_accept():
            return

        # ---- A5 / B6 OPTIONS preflight (no auth) ----
        if method == "OPTIONS":
            self.send_response(204)
            self.send_header("Allow", "GET, POST, PUT, PATCH, DELETE, OPTIONS")
            self._common_headers()
            self.send_header("Access-Control-Max-Age", "86400")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        # ---- B3 auth for protected endpoints ----
        needs_auth = (
            method in ("POST", "PUT", "PATCH", "DELETE")
            or (method == "GET" and re.match(r"^/orders/\d+$", path))
        )
        if needs_auth and not self._auth():
            return

        # ============ /orders ============
        if path == "/orders" and method == "GET":
            # A4 query params: filter/sort/paginate
            filters = {k: qs[k][0] for k in ("status", "customer") if k in qs}
            sort = qs.get("sort", [None])[0]
            try:
                page = int(qs.get("page", ["1"])[0])
                size = int(qs.get("size", ["10"])[0])
                if page < 1 or size < 1 or size > 100:
                    raise ValueError
            except ValueError:
                return self._problem(400, "Bad Request", "page/size invalid")
            items, total = STORE.list(filters or None, sort, page, size)
            return self._send(200,
                              {"items": items, "total": total,
                               "page": page, "size": size},
                              self._rate_headers)

        if path == "/orders" and method == "POST":
            body = self._read_body()
            if body == "__INVALID__":
                return self._problem(400, "Bad Request", "Malformed JSON")
            if not isinstance(body, dict) or not body.get("customer") or not body.get("items"):
                return self._problem(422, "Unprocessable Entity",
                                     "customer and items are required")
            key = self.headers.get("Idempotency-Key")
            status, order = STORE.create(body, key)
            hdrs = dict(self._rate_headers)
            hdrs["Location"] = f"/orders/{order['id']}"           # B2
            hdrs["ETag"] = STORE.etag(order["id"])
            return self._send(status, order, hdrs)

        # ============ /orders/{id} ============
        m = re.match(r"^/orders/(\d+)$", path)
        if m:
            oid = int(m.group(1))

            if method == "GET":
                order = STORE.get(oid)
                if not order:
                    return self._problem(404, "Not Found", f"Order {oid} not found")
                etag = STORE.etag(oid)
                # C1 conditional GET → 304
                if self.headers.get("If-None-Match") == etag:
                    self.send_response(304)
                    self.send_header("ETag", etag)
                    self.send_header("Cache-Control", "public, max-age=60")
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                hdrs = {"ETag": etag, "Cache-Control": "public, max-age=60"}
                hdrs.update(self._rate_headers)
                return self._send(200, order, hdrs)

            if method in ("PUT", "PATCH"):
                body = self._read_body()
                if body == "__INVALID__":
                    return self._problem(400, "Bad Request", "Malformed JSON")
                if not isinstance(body, dict):
                    return self._problem(422, "Unprocessable Entity", "Body must be object")
                st, order = STORE.update(oid, body, self.headers.get("If-Match"))
                if st == 404:
                    return self._problem(404, "Not Found", f"Order {oid} not found")
                if st == 412:
                    return self._problem(412, "Precondition Failed",
                                         "ETag mismatch — resource changed")
                return self._send(200, order, {"ETag": STORE.etag(oid)})

            if method == "DELETE":
                if not STORE.delete(oid):
                    return self._problem(404, "Not Found", f"Order {oid} not found")
                self.send_response(204)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return

        # ============ A2 sub-resources ============
        m = re.match(r"^/orders/(\d+)/cancellation$", path)
        if m and method == "POST":
            st, order = STORE.cancel(int(m.group(1)))
            if st == 404:
                return self._problem(404, "Not Found", "Order not found")
            if st == 409:
                return self._problem(409, "Conflict", "Order already cancelled")
            return self._send(200, order, {"ETag": STORE.etag(order["id"])})

        m = re.match(r"^/orders/(\d+)/checkout$", path)
        if m and method == "POST":
            order = STORE.get(int(m.group(1)))
            if not order:
                return self._problem(404, "Not Found", "Order not found")
            return self._send(200, {"checkout": "ok", "order_id": order["id"]})

        m = re.match(r"^/restaurants/(\d+)/availability$", path)
        if m and method == "POST":
            return self._send(200, {"restaurant": int(m.group(1)),
                                    "availability": self._read_body()})

        # ============ B2 / Q8 — 3xx redirect with Location ============
        m = re.match(r"^/orders/(\d+)/receipt$", path)
        if m and method == "GET":
            oid = int(m.group(1))
            if not STORE.get(oid):
                return self._problem(404, "Not Found", "Order not found")
            self.send_response(303)
            self.send_header("Location", f"/orders/{oid}")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        return self._problem(404, "Not Found", f"No route for {method} {path}")

    # ---------- verbs ----------
    def do_GET(self):     self._route("GET")
    def do_POST(self):    self._route("POST")
    def do_PUT(self):     self._route("PUT")
    def do_PATCH(self):   self._route("PATCH")
    def do_DELETE(self):  self._route("DELETE")
    def do_OPTIONS(self): self._route("OPTIONS")

    def log_message(self, fmt, *args):
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))


def main(port=8085):
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"CampusEats A5 running on http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
