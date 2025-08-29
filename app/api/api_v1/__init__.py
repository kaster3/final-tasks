from fastapi import APIRouter

from app.core import settings

from .some_endpoint import router as endpoint
from .tasks.handlers import router as tasks
from .comments.handlers import router as comments
from .calendar.handlers import router as calendar
from .meetings.handlers import router as meeting

router = APIRouter(
    prefix=settings.base_url.api.v1.prefix,
)

for rout in (endpoint, tasks, comments, calendar, meeting):
    router.include_router(
        router=rout,
    )


@router.get("")
async def root():
    return {"message": "this path is http://127.0.0.1:8000/api/v1"}
