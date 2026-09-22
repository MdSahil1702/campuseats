import json, urllib.request, urllib.error

BASE = "http://localhost:8085"
HDR = {"Authorization": "Bearer campuseats-token",
       "Content-Type": "application/json"}

def _req(method, path, body=None, headers=None):
    req = urllib.request.Request(BASE + path, method=method,
                                 data=json.dumps(body).encode() if body else None,
                                 headers=headers or HDR)
    try:
        r = urllib.request.urlopen(req)
        return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()

def test_options_allow_header():
    st, h, _ = _req("OPTIONS", "/orders", headers={})
    assert st == 204
    assert "Allow" in h

def test_put_replaces_order():
    st, h, _ = _req("POST", "/orders",
                    {"customer": "t", "items": [{"id": "x"}]})
    oid = json.loads(h and _ or b'{}') if False else None  # created in POST /orders test
    # simple: fetch last id
    _, _, raw = _req("GET", "/orders")
    oid = json.loads(raw)["items"][-1]["id"]
    st, h, _ = _req("PUT", f"/orders/{oid}", {"status": "PAID"})
    assert st == 200
    assert "ETag" in h

def test_override_header():
    st, h, _ = _req("POST", "/orders",
                    {"customer": "t", "items": [{"id": "y"}]})
    _, _, raw = _req("GET", "/orders")
    oid = json.loads(raw)["items"][-1]["id"]
    st, h, _ = _req("POST", f"/orders/{oid}",
                    {"status": "PAID"},
                    headers={**HDR, "X-HTTP-Method-Override": "PUT"})
    assert st == 200
