from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api_v1.comments.dto import CommentCreateRequest
from app.core.database.models import TaskComment
from app.core.repository.interfaces.comment import IDBCommentRepository


class SQLAlchemyCommentRepository(IDBCommentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, comment_data: CommentCreateRequest, cur_user_id: int) -> TaskComment:
        comment = TaskComment(**comment_data.model_dump(), author_id=cur_user_id)
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment