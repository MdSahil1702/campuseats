import json, urllib.request, urllib.error

BASE = "http://localhost:8085"
HDR = {"Authorization": "Bearer campuseats-token",
       "Content-Type": "application/json"}

def test_304():
    req = urllib.request.Request(BASE + "/orders",
        data=json.dumps({"customer": "c", "items": [{"id": "1"}]}).encode(),
        method="POST", headers=HDR)
    urllib.request.urlopen(req)
    req = urllib.request.Request(BASE + "/orders", headers=HDR)
    oid = json.loads(urllib.request.urlopen(req).read())["items"][-1]["id"]
    req = urllib.request.Request(BASE + f"/orders/{oid}", headers=HDR)
    etag = urllib.request.urlopen(req).headers["ETag"]
    req = urllib.request.Request(BASE + f"/orders/{oid}",
        headers={**HDR, "If-None-Match": etag})
    try:
        urllib.request.urlopen(req)
        assert False, "expected 304"
    except urllib.error.HTTPError as e:
        assert e.code == 304

def test_412():
    req = urllib.request.Request(BASE + "/orders",
        data=json.dumps({"customer": "c", "items": [{"id": "1"}]}).encode(),
        method="POST", headers=HDR)
    urllib.request.urlopen(req)
    req = urllib.request.Request(BASE + "/orders", headers=HDR)
    oid = json.loads(urllib.request.urlopen(req).read())["items"][-1]["id"]
    req = urllib.request.Request(BASE + f"/orders/{oid}",
        data=json.dumps({"status": "PAID"}).encode(),
        method="PUT",
        headers={**HDR, "If-Match": '"stale-0000"'})
    try:
        urllib.request.urlopen(req)
        assert False, "expected 412"
    except urllib.error.HTTPError as e:
        assert e.code == 412