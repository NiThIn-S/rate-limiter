#!/usr/bin/env bash

# Test script: calls GET /api/test/ in a loop (useful for rate-limit testing)

URL="${1:-http://0.0.0.0:8001/api/test/}"
COUNT="${2:-120}"

echo "Testing: $URL"
echo "Requests: $COUNT"
echo "---"

for i in $(seq 1 "$COUNT"); do
  printf "[%3d] " "$i"
  curl -s -w " status=%{http_code} time=%{time_total}s\n" -o /dev/null \
    -X 'GET' \
    "$URL" \
    -H 'accept: application/json' \
    -H 'x-api-key: 123'
  sleep 1

done

echo "---"
echo "Done."
