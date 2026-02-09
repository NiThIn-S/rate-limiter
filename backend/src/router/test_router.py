from fastapi import APIRouter, status, Header
from config.logger import log

test_router = APIRouter(
    prefix="/test",
    tags=["Test API"]
)

# --- Test endpoint ---
@test_router.get("/", status_code=status.HTTP_200_OK)
async def test(
    x_api_key: str = Header(..., description="API key"),
):
    log.info("*****Test endpoint called.*****")
    return {"message": "Hello, World!"}
    
