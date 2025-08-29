from typing import AsyncGenerator

from dishka import Provider, Scope, provide
from httpx import AsyncClient

from app.api.api_v1.tasks.handlers import TaskService
from app.core.auth.jwt import JWTHelper
from app.core.repository.implementation.calendar import SQLAlchemyCalendarRepository
from app.core.repository.implementation.comment import SQLAlchemyCommentRepository
from app.core.repository.implementation.meeting import SQLAlchemyMeetingRepository
from app.core.repository.implementation.task import SQLAlchemyRepository
from app.core.repository.interfaces.calendar import IDBCalendarRepository
from app.core.repository.interfaces.comment import IDBCommentRepository
from app.core.repository.interfaces.meeting import IDBMeetingRepository
from app.core.repository.interfaces.task import IDBTaskRepository
from app.core.services.calendar import CalendarService
from app.core.services.comment import CommentService
from app.core.services.meeting import MeetingService
from app.core.services.user_client import UserServiceClient


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    task_repo = provide(SQLAlchemyRepository, provides=IDBTaskRepository)
    comment_repo = provide(SQLAlchemyCommentRepository, provides=IDBCommentRepository)
    calendar_repo = provide(SQLAlchemyCalendarRepository, provides=IDBCalendarRepository)
    meeting_repo = provide(SQLAlchemyMeetingRepository, provides=IDBMeetingRepository)

    task_service = provide(TaskService)
    user_client = provide(UserServiceClient)
    comment_servie = provide(CommentService)
    calendar_service = provide(CalendarService)
    meeting_service = provide(MeetingService)
    jwt_service = provide(JWTHelper)

    @provide(scope=Scope.REQUEST)
    async def get_async_httpx_session(
            self,
    ) -> AsyncGenerator[AsyncClient, None]:
        async with AsyncClient(timeout=30.0) as client:
            yield client


