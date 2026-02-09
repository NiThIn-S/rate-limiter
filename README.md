# Rate Limiter API

FastAPI backend with Redis-backed rate limiting. Requests are limited per API key within a configurable window.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- (Optional) Bash, for running the test script

## Setup

### 1. Environment variables

Create a `.env` file in the **project root** (same directory as `docker-compose.yml`):

```env
REDIS_PASSWORD=your_redis_password
# Optional:
# REDIS_USERNAME=
# ENV=dev
# LOG_LEVEL=INFO
```

`REDIS_PASSWORD` is required when using Docker Compose so Redis starts with authentication.

### 2. Start services

From the project root:

```bash
docker compose up -d
```

This starts:

- **Redis** on port `6380` (host) → `6379` (container), with optional password
- **Backend** on port `8000`, waiting for Redis to be healthy

Check that both are running:

```bash
docker compose ps
```

### 3. Verify the API

```bash
curl -s -X GET 'http://0.0.0.0:8000/api/test/' \
  -H 'accept: application/json' \
  -H 'x-api-key: 123'
```

You should get a JSON response (e.g. `{"message":"ok"}` or similar).

## Running the rate-limit test

Use the included shell script to send many requests in a loop and observe rate limiting (e.g. 429 responses after the limit is hit).

**From the project root:**

```bash
./test_api.sh
```

- **Default:** 120 requests to `http://0.0.0.0:8000/api/test/` with a 1-second delay between requests (matches Docker Compose).
- **Custom URL and count:**

  ```bash
  ./test_api.sh http://0.0.0.0:8000/api/test/ 50
  ```

**Example output:**

```
Testing: http://0.0.0.0:8000/api/test/
Requests: 50
---
[  1]  status=200 time=0.012s
[  2]  status=200 time=0.008s
...
[ 61]  status=429 time=0.005s
---
Done.
```

Once the rate limit is exceeded, you should see `status=429`. Limits are controlled by `RATE_LIMIT_REQUESTS` and `RATE_LIMIT_WINDOW` (see backend config).

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `RATE_LIMIT_REQUESTS` | 60 | Max requests per window |
| `RATE_LIMIT_WINDOW` | 60 | Window length (seconds) |
| `RATE_LIMIT_BACKEND` | memory | `memory` (per-worker) or `redis` (global) |
| `REDIS_HOST` | localhost | Redis host (use `redis` in Docker) |
| `REDIS_PORT` | 6379 | Redis port |
| `REDIS_PASSWORD` | — | Redis password (required in Docker setup) |

## Stopping

```bash
docker compose down
```

To remove the Redis data volume as well:

```bash
docker compose down -v
```
