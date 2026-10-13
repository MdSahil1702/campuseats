import json, urllib.request, urllib.error
BASE = "http://localhost:8086"
HDR = {"Authorization": "Bearer campuseats-token",
       "Content-Type": "application/json"}


def test_problem_shape_on_404():
    req = urllib.request.Request(BASE + "/orders/9999", headers=HDR)
    try:
        urllib.request.urlopen(req)
        assert False
    except urllib.error.HTTPError as e:
        body = json.loads(e.read())
        assert e.headers["Content-Type"].startswith("application/problem+json")
        assert body["status"] == 404
        assert "type" in body and "title" in body and "detail" in body


def test_problem_shape_on_422():
    req = urllib.request.Request(
        BASE + "/orders",
        data=json.dumps({"customer":"","address":"","items":[]}).encode(),
        method="POST", headers=HDR)
    try:
        urllib.request.urlopen(req)
        assert False
    except urllib.error.HTTPError as e:
        body = json.loads(e.read())
        assert body["status"] == 422
        assert "errors" in body and len(body["errors"]) >= 1
