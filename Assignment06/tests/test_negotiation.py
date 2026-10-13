import json, urllib.request, urllib.error
BASE = "http://localhost:8086"
HDR = {"Authorization": "Bearer campuseats-token",
       "Content-Type": "application/json"}


def _create():
    req = urllib.request.Request(
        BASE + "/orders",
        data=json.dumps({"customer":"c","address":"A",
                         "items":[{"id":"x","qty":1}]}).encode(),
        method="POST", headers=HDR)
    urllib.request.urlopen(req)


def test_xml_response():
    _create()
    req = urllib.request.Request(BASE + "/orders/1",
                                 headers={**HDR, "Accept": "application/xml"})
    r = urllib.request.urlopen(req)
    assert "application/xml" in r.headers["Content-Type"]
    assert r.read().startswith(b"<?xml")


def test_406_on_bad_accept():
    req = urllib.request.Request(BASE + "/orders/1",
                                 headers={**HDR, "Accept": "text/plain"})
    try:
        urllib.request.urlopen(req)
        assert False
    except urllib.error.HTTPError as e:
        assert e.code == 406
        assert e.headers["Content-Type"].startswith("application/problem+json")
