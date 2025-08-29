from fastapi import APIRouter

from app.api.api_v1 import router as api_v1_router
from app.core import settings

router = APIRouter(
    prefix=settings.base_url.api.prefix,
)

for rout in (api_v1_router,):
    router.include_router(
        router=rout,
    )


@router.get("")
async def root():
    return {"message": "this path is http://127.0.0.1:8000/api"}
