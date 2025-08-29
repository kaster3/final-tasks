from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status, Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.api.api_v1.tasks.dto import TaskCreate, TaskUpdate, TaskRead
from app.core.auth.jwt import JWTHelper
from app.core.auth.methods import http_bearer
from app.core.services.task import TaskService
from app.core.settings import settings

router = APIRouter(
    prefix=settings.base_url.api.v1.tasks,
    tags=["Tasks"],
)


@router.get(
    path="/{tasks_id}",
    response_model=TaskRead,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_task(task_id: int, service: FromDishka[TaskService]):
    return await service.get_task(task_id=task_id)


@router.post(
    path="",
    response_model=TaskCreate,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_task(
        task_data: TaskCreate,
        service: FromDishka[TaskService],
        jwt_helper: FromDishka[JWTHelper],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
):
    cur_user_id = jwt_helper.get_user_id(token=credentials.credentials)
    return await service.create_task(
        task_data=task_data,
        cur_user_id=cur_user_id,
    )


@router.patch(
    path="/{task_id}",
    response_model=TaskUpdate,
    status_code=status.HTTP_200_OK,
)
@inject
async def update_task(
        task_id: int,
        task_data: TaskUpdate,
        service: FromDishka[TaskService],
):
    return await service.update_task(task_id=task_id, task_data=task_data)


@router.delete(
    path="/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def del_task(
        task_id: int,
        service: FromDishka[TaskService],
):
    return await service.del_task(task_id=task_id)








