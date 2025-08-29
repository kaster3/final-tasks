from app.api.api_v1.comments.dto import CommentCreateRequest
from app.core.database.models import TaskComment
from app.core.repository.interfaces.comment import IDBCommentRepository
from app.core.services.task import TaskService




class CommentService:
    def __init__(
            self,
            task_service: TaskService,
            comment_repo: IDBCommentRepository,
    ) -> None:
        self.task_service = task_service
        self.comment_repo = comment_repo

    async def create_comment(
            self,
            comment_data: CommentCreateRequest,
            cur_user_id: int
    ) -> TaskComment:
        await self.task_service.get_task(task_id=comment_data.task_id)
        comment = await self.comment_repo.create(
            comment_data=comment_data,
            cur_user_id=cur_user_id,
        )
        return comment