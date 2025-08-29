from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status, Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.api.api_v1.comments.dto import CommentCreateResponse, CommentCreateRequest
from app.core.auth.jwt import JWTHelper
from app.core.auth.methods import http_bearer
from app.core.services.comment import CommentService
from app.core.settings import settings



router = APIRouter(
    prefix=settings.base_url.api.v1.comments,
    tags=["Comments"],
)

@router.post(
    path="",
    response_model=CommentCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_comment(
        comment_data: CommentCreateRequest,
        service: FromDishka[CommentService],
        jwt_helper: FromDishka[JWTHelper],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
):
    cur_user_id = jwt_helper.get_user_id(token=credentials.credentials)
    return await service.create_comment(comment_data=comment_data, cur_user_id=cur_user_id)




