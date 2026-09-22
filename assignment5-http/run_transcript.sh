#!/usr/bin/env bash
# Usage: python server5.py & ; bash run_transcript.sh > curl-transcript.txt
B=http://localhost:8085
T="Authorization: Bearer campuseats-token"
H="Content-Type: application/json"
IDEM="Idempotency-Key: demo-key-1"

echo "=== 1) CREATE (201 + Location) ==="
curl -v -X POST $B/orders -H "$T" -H "$H" -H "$IDEM" \
     -d '{"customer":"sahil","items":[{"id":"pizza","qty":2}]}'

echo; echo "=== 2) SAME Idempotency-Key repeat (same 201, no duplicate) ==="
curl -v -X POST $B/orders -H "$T" -H "$H" -H "$IDEM" \
     -d '{"customer":"sahil","items":[{"id":"pizza","qty":2}]}'

echo; echo "=== 3) Conditional GET with matching ETag → 304 ==="
ETAG=$(curl -s -D - -o /dev/null $B/orders/1 -H "$T" | awk '/^ETag/{print $2}' | tr -d '\r')
echo "Captured ETag: $ETAG"
curl -v $B/orders/1 -H "$T" -H "If-None-Match: $ETAG"

echo; echo "=== 4) Conditional PUT with stale If-Match → 412 ==="
curl -v -X PUT $B/orders/1 -H "$T" -H "$H" \
     -H 'If-Match: "stale-0000"' -d '{"status":"PAID"}'

echo; echo "=== 5) 400 Malformed JSON ==="
curl -v -X POST $B/orders -H "$T" -H "$H" -d '{"customer":'

echo; echo "=== 6) 404 Missing order ==="
curl -v $B/orders/9999 -H "$T"

echo; echo "=== 7) 401 Missing token ==="
curl -v -X POST $B/orders -H "$H" -d '{"customer":"x","items":[]}'

echo; echo "=== 8) OPTIONS preflight ==="
curl -v -X OPTIONS $B/orders -H 'Origin: https://other.example'

echo; echo "=== 9) 406 Not Acceptable ==="
curl -v $B/orders/1 -H "$T" -H 'Accept: application/xml'
