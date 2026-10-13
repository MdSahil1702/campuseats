#!/usr/bin/env bash
set -e
python3 ../server6.py & SRV=$!
sleep 2
OUT=$(bash ../run_transcript.sh)
echo "$OUT" | grep -q "201 Created"        || (echo "missing 201"; kill $SRV; exit 1)
echo "$OUT" | grep -q "400 Bad Request"    || (echo "missing 400"; kill $SRV; exit 1)
echo "$OUT" | grep -q "401 Unauthorized"   || (echo "missing 401"; kill $SRV; exit 1)
echo "$OUT" | grep -q "404 Not Found"      || (echo "missing 404"; kill $SRV; exit 1)
echo "$OUT" | grep -q "406 Not Acceptable" || (echo "missing 406"; kill $SRV; exit 1)
echo "$OUT" | grep -q "409 Conflict"       || (echo "missing 409"; kill $SRV; exit 1)
echo "$OUT" | grep -q "422 Unprocessable"  || (echo "missing 422"; kill $SRV; exit 1)
echo "$OUT" | grep -q "429 Too Many"       || (echo "missing 429"; kill $SRV; exit 1)
echo "$OUT" | grep -qi "application/xml"   || (echo "missing XML"; kill $SRV; exit 1)
kill $SRV 2>/dev/null || true
echo "All A6 status codes present."
