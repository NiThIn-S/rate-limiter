import asyncio
import time
from collections import deque

from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware

from config.logger import log
from config.constants import RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW


# In-memory sliding window state (asyncio.Lock for concurrency safety)
_lock = asyncio.Lock()
_windows: dict[str, deque[float]] = {}

EXTRA_PUBLIC_ENDPOINTS = [
    "/liveness",
]

def _get_api_key(request: Request) -> str:
    """Get user key from request."""
    api_key = request.headers.get("X-API-KEY")
    if api_key:
        return api_key
    else:
        log.error(f"Unknown API key for request: {request}")
        return "unknown"


async def _check_rate_limit(request: Request) -> tuple[bool, str]:
    """Sliding window: allow if requests in last RATE_LIMIT_WINDOW_SEC < RATE_LIMIT_N. Returns (allowed, retry_after_sec or remaining)."""
    key = _get_api_key(request)
    now = time.monotonic()
    async with _lock:
        if key not in _windows:
            _windows[key] = deque(maxlen=RATE_LIMIT_REQUESTS * 2)
        q = _windows[key]
        while q and q[0] < now - RATE_LIMIT_WINDOW:
            q.popleft()
        if len(q) >= RATE_LIMIT_REQUESTS:
            retry_after = max(0, int(q[0] + RATE_LIMIT_WINDOW - now))
            return False, str(retry_after)
        q.append(now)
        remaining = RATE_LIMIT_REQUESTS - len(q)
        return True, str(remaining)


class RateLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            request.state.is_public = False
            # Allow CORS preflight to pass through quickly
            if request.method == "OPTIONS":
                request.state.is_public = True
                return await call_next(request)

            elif request.url.path in EXTRA_PUBLIC_ENDPOINTS:
                request.state.is_public = True
                return await call_next(request)
            else:
                is_allowed, value = await _check_rate_limit(request)
                if not is_allowed:
                    return JSONResponse(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        headers={"Retry-After": value},
                        content={"detail": "Rate limit exceeded"},
                    )
            return await call_next(request)
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": str(e)})
