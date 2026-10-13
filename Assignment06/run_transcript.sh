#!/usr/bin/env bash
B=http://localhost:8086
T="Authorization: Bearer campuseats-token"
J="Content-Type: application/json"

echo "=== 1) SUCCESS: POST /orders -> 201 + Location ==="
curl -i -X POST $B/orders -H "$T" -H "$J" \
  -d '{"customer":"sahil","address":"Hostel A","items":[{"id":"pizza","qty":2}]}'

echo; echo "=== 2) FAIL 400: malformed JSON ==="
curl -i -X POST $B/orders -H "$T" -H "$J" -d '{"customer":'

echo; echo "=== 3) FAIL 401: missing token ==="
curl -i -X POST $B/orders -H "$J" \
  -d '{"customer":"x","address":"y","items":[{"id":"a","qty":1}]}'

echo; echo "=== 4) FAIL 406: bad Accept ==="
curl -i $B/orders/1 -H "Accept: text/plain"

echo; echo "=== 5) FAIL 422: empty cart ==="
curl -i -X POST $B/orders -H "$T" -H "$J" \
  -d '{"customer":"sahil","address":"A","items":[]}'

echo; echo "=== 6) FAIL 422: qty <= 0 ==="
curl -i -X POST $B/orders -H "$T" -H "$J" \
  -d '{"customer":"sahil","address":"A","items":[{"id":"pizza","qty":0}]}'

echo; echo "=== 7) FAIL 404: unknown order ==="
curl -i $B/orders/9999

echo; echo "=== 8) FAIL 409: illegal transition (cancel twice) ==="
curl -i -X POST $B/orders/1/cancellation -H "$T"
curl -i -X POST $B/orders/1/cancellation -H "$T"

echo; echo "=== 9) FAIL 429: rate limit + Retry-After ==="
curl -i $B/rate

echo; echo "=== 10) NEGOTIATION: Accept: application/xml ==="
curl -i -X POST $B/orders -H "$T" -H "$J" -H "Accept: application/xml" \
  -d '{"customer":"sahil","address":"A","items":[{"id":"pizza","qty":1}]}'
