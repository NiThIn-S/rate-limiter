import os
import dotenv

dotenv.load_dotenv()

APP_ENV = os.getenv('ENV', 'dev')
PORT = int(os.getenv('PORT', '8000'))
WORKERS = int(os.getenv('WORKERS', '3'))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
SERVICE_NAME = os.getenv('SERVICE_NAME', 'rate-limiter')

RATE_LIMIT_REQUESTS = int(os.getenv('RATE_LIMIT_REQUESTS', '60'))
RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', '60')) # in seconds

# TODO: For future use, currently only memory is supported per worker

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_USERNAME = os.getenv('REDIS_USERNAME', None)
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
if not REDIS_PASSWORD:
    REDIS_PASSWORD = None
if not REDIS_USERNAME:
    REDIS_USERNAME = None

REDIS_KEY_PREFIX = "rate-limiter:"

# Rate limit: "memory" (per-worker) or "redis" (global across workers)
RATE_LIMIT_BACKEND = os.getenv("RATE_LIMIT_BACKEND", "memory").lower()
RATE_LIMIT_N = int(os.getenv("RATE_LIMIT_N", "60"))
RATE_LIMIT_WINDOW_SEC = int(os.getenv("RATE_LIMIT_WINDOW_SEC", "60"))

