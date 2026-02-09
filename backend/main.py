import asyncio
import uvicorn
from logging.config import dictConfig # before fastapi
from contextlib import asynccontextmanager

from fastapi.responses import JSONResponse
from fastapi import FastAPI, status, Request
from fastapi.middleware.cors import CORSMiddleware

import config
from config.logger import log, log_config

from src import router
from src.lib.exception_handler import register_exception
from src.middlewares.rate_limiter import RateLimiterMiddleware

origins = ["*"]

dictConfig(log_config)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application start eatablish redis/in-mmeory DB connection if necessary.
    """
    log.info("*****Application started.*****")
    yield
    log.warning("*****Application shutting down.*****")


if config.APP_ENV == "prod":
    openapi_url = None
else:
    openapi_url = "/openapi.json"
    log.warning("Non production environment - OpenAPI docs exposed")

app = FastAPI(
    title=config.SERVICE_NAME,
    version="1.0.0",
    lifespan=lifespan,
    openapi_url=openapi_url,
)


# CORS origin config.
app.add_middleware(RateLimiterMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception(app=app)
log.info("*****Logger initialized.*****")

@app.get("/liveness", status_code=status.HTTP_200_OK)
async def liveness():
    return {"message": "OK"}


# Initializing all routers with prefix.
router_prefix = "/api"

app.include_router(router.test_router, prefix=router_prefix)

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        port=config.PORT,
        host='0.0.0.0',
        workers=1,
        # reload=True,
    )
