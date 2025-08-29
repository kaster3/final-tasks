from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from starlette import status

from app.core.auth.jwt import JWTHelper
from app.core.auth.methods import http_bearer
from app.core.database.models import Meeting
from app.core.services.meeting import MeetingService
from app.core.settings import settings
from app.api.api_v1.meetings.dto import MeetingCreateRequest, MeetingUpdate, MeetingRead

router = APIRouter(
    prefix=settings.base_url.api.v1.meetings,
    tags=["Meetings"],
)


@router.get(
    path="/{meeting_id}",
    response_model=MeetingRead,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_meeting(meeting_id: int, service: FromDishka[MeetingService]):
    return await service.get_meeting(meeting_id=meeting_id)


@router.post(
    path="",
    response_model=MeetingRead,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_meeting(
        meeting_data: MeetingCreateRequest,
        service: FromDishka[MeetingService],
        jwt_helper: FromDishka[JWTHelper],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
):
    cur_user_id = jwt_helper.get_user_id(token=credentials.credentials)
    return await service.create_meeting(meeting_data=meeting_data)


@router.patch(
    path="/{meeting_id}",
    response_model=MeetingUpdate,
    status_code=status.HTTP_200_OK,
)
@inject
async def update_meeting(
        meeting_id: int,
        meeting_data: MeetingUpdate,
        service: FromDishka[MeetingService],
        jwt_helper: FromDishka[JWTHelper],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
):
    jwt_helper.get_user_id(token=credentials.credentials)
    return await service.update_meeting(meeting_id=meeting_id, meeting_data=meeting_data)


@router.delete(
    path="/{meeting_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def del_meeting(
        meeting_id: int,
        service: FromDishka[MeetingService],
        jwt_helper: FromDishka[JWTHelper],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
):
    jwt_helper.get_user_id(token=credentials.credentials)
    return await service.delete_meeting(meeting_id=meeting_id)
