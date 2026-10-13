import json, urllib.request, urllib.error
BASE = "http://localhost:8086"
HDR = {"Authorization": "Bearer campuseats-token",
       "Content-Type": "application/json"}


def _post(body):
    req = urllib.request.Request(BASE + "/orders",
        data=json.dumps(body).encode(), method="POST", headers=HDR)
    try:
        urllib.request.urlopen(req)
        return 201, None
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def test_empty_cart_422():
    st, body = _post({"customer":"c","address":"A","items":[]})
    assert st == 422
    assert any("items" in e["field"] for e in body["errors"])


def test_qty_zero_422():
    st, body = _post({"customer":"c","address":"A","items":[{"id":"x","qty":0}]})
    assert st == 422
    assert any("qty" in e["field"] for e in body["errors"])


def test_missing_address_422():
    st, body = _post({"customer":"c","items":[{"id":"x","qty":1}]})
    assert st == 422
    assert any(e["field"] == "address" for e in body["errors"])


def test_collects_all_errors():
    st, body = _post({"customer":"","items":[{"id":"","qty":0}]})
    assert st == 422
    assert len(body["errors"]) >= 3
