
import json, os, re, sys, traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from problem import send_problem, problem_body
from validation import validate
from xml_render import to_xml

VALID_TOKEN = "campuseats-token"


class Store:
  
    def __init__(self):
        self.orders = {}
        self.idem = {}
        self.seq = 0

    def create(self, payload, key=None):
        if key and key in self.idem:
            return self.idem[key]
        self.seq += 1
        oid = self.seq
        order = {
            "id": oid,
            "customer": payload["customer"],
            "address": payload["address"],
            "items": payload["items"],
            "status": "PLACED",
        }
        self.orders[oid] = order
        result = (201, order)
        if key:
            self.idem[key] = result
        return result

    def get(self, oid):
        return self.orders.get(oid)

    def cancel(self, oid):
        order = self.orders.get(oid)
        if not order:
            return 404, None, "order-not-found"
        if order["status"] == "CANCELLED":
            return 409, order, "illegal-transition"
        if order["status"] in ("SHIPPED", "DELIVERED"):
            return 409, order, "illegal-transition"
        order["status"] = "CANCELLED"
        return 200, order, None


STORE = Store()


class Handler(BaseHTTPRequestHandler):
    server_version = "CampusEats/6.0"
    protocol_version = "HTTP/1.1"

    # ---------- helpers ----------
    def _common(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Strict-Transport-Security",
                         "max-age=31536000; includeSubDomains")
        self.send_header("Access-Control-Allow-Origin", "*")

    def _send_json(self, status, body, headers=None):
        data = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self._common()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        if headers:
            for k, v in headers.items():
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def _send_xml(self, status, data):
        payload = to_xml("response", data)
        self.send_response(status)
        self._common()
        self.send_header("Content-Type", "application/xml; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _negotiate(self):
        """C3: honour Accept. Return 'json', 'xml', or None (=> 406)."""
        accept = self.headers.get("Accept", "*/*")
        if "application/xml" in accept:
            return "xml"
        if "application/json" in accept or "*/*" in accept:
            return "json"
        return None

    def _read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return None, None
        raw = self.rfile.read(length)
        try:
            return json.loads(raw), None
        except json.JSONDecodeError as e:
            return None, str(e)

    def _auth(self):
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer ") or len(auth) <= len("Bearer "):
            send_problem(self, "unauthorized", "Bearer token required")
            return False
        return True

    # ---------- routing ----------
    def _route(self, method):
        parsed = urlparse(self.path)
        path, qs = parsed.path, parse_qs(parsed.query)

        # C3 negotiation — before anything else
        fmt = self._negotiate()
        if fmt is None:
            send_problem(self, "not-acceptable",
                         "Supported: application/json, application/xml",
                         headers={"Vary": "Accept"})
            return

        # POST /orders
        if path == "/orders" and method == "POST":
            if not self._auth():
                return
            body, err = self._read_json()
            if err:
                send_problem(self, "malformed-json", f"JSON parse error: {err}")
                return
            ok, errors = validate(body)
            if not ok:
                send_problem(self, "validation-failed",
                             "One or more fields failed validation.",
                             errors=errors)
                return
            key = self.headers.get("Idempotency-Key")
            status, order = STORE.create(body, key)
            headers = {"Location": f"/orders/{order['id']}"}
            if fmt == "xml":
                self._send_xml(status, order)
            else:
                self._send_json(status, order, headers)
            return

        # GET /orders/{id}
        m = re.match(r"^/orders/(\d+)$", path)
        if m and method == "GET":
            oid = int(m.group(1))
            order = STORE.get(oid)
            if not order:
                send_problem(self, "order-not-found", f"Order {oid} does not exist.")
                return
            if fmt == "xml":
                self._send_xml(200, order)
            else:
                self._send_json(200, order)
            return

        # POST /orders/{id}/cancellation  (illegal transition demo)
        m = re.match(r"^/orders/(\d+)/cancellation$", path)
        if m and method == "POST":
            if not self._auth():
                return
            oid = int(m.group(1))
            st, order, kind = STORE.cancel(oid)
            if kind == "order-not-found":
                send_problem(self, "order-not-found", f"Order {oid} does not exist.")
                return
            if kind == "illegal-transition":
                send_problem(self, "illegal-transition",
                             f"Cannot cancel order in state {order['status']}.")
                return
            self._send_json(200, order)
            return

        # Rate-limit demo (429 + Retry-After)
        if path == "/rate" and method == "GET":
            self.send_response(429)
            self._common()
            self.send_header("Content-Type", "application/problem+json; charset=utf-8")
            self.send_header("Retry-After", "30")
            body = problem_body("rate-limited", "Per-client budget exceeded.")
            data = json.dumps(body).encode()
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        # 404 fallback
        send_problem(self, "order-not-found", f"No route for {method} {path}")

    # ---------- B4: never leak internals ----------
    def _safe(self, method):
        try:
            self._route(method)
        except Exception:
            traceback.print_exc()
            try:
                send_problem(self, "internal-error",
                             "An unexpected error occurred.")
            except Exception:
                pass

    def do_GET(self):     self._safe("GET")
    def do_POST(self):    self._safe("POST")
    def do_PUT(self):     self._safe("PUT")
    def do_PATCH(self):   self._safe("PATCH")
    def do_DELETE(self):  self._safe("DELETE")
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Allow", "GET, POST, OPTIONS")
        self._common()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))


def main(port=8086):
    srv = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"CampusEats A6 running on http://localhost:{port}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
