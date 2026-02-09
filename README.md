# Rate Limiter API — Backend only (no redis DB)

Run the FastAPI backend locally with **in-memory** rate limiting. No Redis or Docker required.

## Prerequisites

- **Python 3.12+**
- [uv](https://docs.astral.sh/uv/) (or use `pip` and a venv)

## Setup

### 1. Go to the backend directory

```bash
cd backend
```

### 2. Install dependencies

With **uv** (recommended):

```bash
uv sync
```

With **pip**:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

### 3. (Optional) Environment variables

Create a `backend/.env` or export variables. Defaults are enough to run:

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 8000 | Server port |
| `RATE_LIMIT_REQUESTS` | 60 | Max requests per window |
| `RATE_LIMIT_WINDOW` | 60 | Window length (seconds) |
| `RATE_LIMIT_BACKEND` | memory | Use `memory` (no Redis) or `redis` |


## Run the backend

From the **backend** directory:

```bash
uv run python main.py
```

Server will be at **http://0.0.0.0:8000** (or the port you set).

### Quick check

```bash
curl -s -X GET 'http://0.0.0.0:8000/api/test/' \
  -H 'accept: application/json' \
  -H 'x-api-key: 123'
```

## Run the rate-limit test

From the **project root** (parent of `backend/`):

```bash
./test_api.sh
```

- Default: 120 requests to `http://0.0.0.0:8000/api/test/` with 1s delay.
- Custom URL and count:

  ```bash
  ./test_api.sh http://0.0.0.0:8000/api/test/ 80
  ```

You should see `status=200` until the limit is hit, then `status=429`.

## Summary

| Step | Command |
|------|---------|
| Install deps | `cd backend && uv sync` |
| Start backend | `uv run python main.py` |
| Test | From repo root: `./test_api.sh` |
