#!/usr/bin/env bash
# Runs curl-transcript and asserts key status codes appear.
set -e
cd "$(dirname "$0")/.."
python3 server5.py & SRV=$!
sleep 2
OUT=$(bash run_transcript.sh)
echo "$OUT" | grep -q "201 Created"        || (echo "missing 201"; kill $SRV; exit 1)
echo "$OUT" | grep -q "304 Not Modified"   || (echo "missing 304"; kill $SRV; exit 1)
echo "$OUT" | grep -q "412 Precondition"   || (echo "missing 412"; kill $SRV; exit 1)
echo "$OUT" | grep -q "400 Bad Request"    || (echo "missing 400"; kill $SRV; exit 1)
echo "$OUT" | grep -q "404 Not Found"      || (echo "missing 404"; kill $SRV; exit 1)
echo "$OUT" | grep -q "401 Unauthorized"   || (echo "missing 401"; kill $SRV; exit 1)
kill $SRV
echo "All required status codes present."
