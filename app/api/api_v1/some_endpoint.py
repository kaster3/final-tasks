from fastapi import APIRouter

from app.core import settings

router = APIRouter(
    prefix=settings.base_url.api.v1.endpoint,
    tags=["some_endpoint"],
)


@router.get("")
async def get_endpoint():
    return {"message": "Hello, this is the endpoint you requested!"}
