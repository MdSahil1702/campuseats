import json, urllib.request, urllib.error
BASE = "http://localhost:8086"
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


def test_create_201_with_location():
    st, h, _ = _req("POST", "/orders",
        {"customer": "c", "address": "A", "items": [{"id": "x", "qty": 1}]})
    assert st == 201
    assert h["Location"].startswith("/orders/")


def test_missing_order_404():
    st, _, _ = _req("GET", "/orders/9999")
    assert st == 404


def test_missing_token_401():
    st, _, _ = _req("POST", "/orders",
        {"customer": "c", "address": "A", "items": [{"id": "x", "qty": 1}]},
        headers={"Content-Type": "application/json"})
    assert st == 401


def test_bad_accept_406():
    st, _, _ = _req("GET", "/orders/1", headers={**HDR, "Accept": "text/plain"})
    assert st == 406


def test_rate_limit_429_with_retry_after():
    st, h, _ = _req("GET", "/rate")
    assert st == 429
    assert "Retry-After" in h
