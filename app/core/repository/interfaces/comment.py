from abc import abstractmethod

from typing import Protocol

from app.api.api_v1.comments.dto import CommentCreateRequest
from app.core.database.models import TaskComment


class IDBCommentRepository(Protocol):
    @abstractmethod
    async def create(self, comment_data: CommentCreateRequest, cur_user_id: int) -> TaskComment:
        raise NotImplementedError