from datetime import date
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query, Depends
from fastapi.security import HTTPAuthorizationCredentials
from starlette import status

from app.api.api_v1.calendar.dto import CalendarResponse, CalendarCreateRequest
from app.core.auth.jwt import JWTHelper
from app.core.auth.methods import http_bearer
from app.core.services.calendar import CalendarService
from app.core.settings import settings


router = APIRouter(
    prefix=settings.base_url.api.v1.calendar,
    tags=["Calendar"],
)

@router.get(
    "/events",
    response_model=list[CalendarResponse],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_my_events(
        service: FromDishka[CalendarService],
        jwt_helper: FromDishka[JWTHelper],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
        start_date: date = Query(..., description="Начальная дата периода"),
        end_date: date = Query(..., description="Конечная дата периода"),
):
    cur_user_id = jwt_helper.get_user_id(token=credentials.credentials)
    return await service.get_user_events(cur_user_id, start_date, end_date)

@router.post(
    "/events",
    response_model=CalendarResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_event(
        event_data: CalendarCreateRequest,
        service: FromDishka[CalendarService],
        jwt_helper: FromDishka[JWTHelper],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
):
    cur_user_id = jwt_helper.get_user_id(token=credentials.credentials)
    return await service.create_event(event_data=event_data)