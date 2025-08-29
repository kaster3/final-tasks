from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api_v1.tasks.dto import TaskCreate, TaskUpdate
from app.core.database.models import Task
from app.core.repository.interfaces.task import IDBTaskRepository


class SQLAlchemyRepository(IDBTaskRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_task(self, task_id: int) -> Task | None:
        task = await self.session.get(Task, task_id)
        return task

    async def create_task(self, task_data: TaskCreate, cur_user_id: int) -> Task:
        task = Task(**task_data.model_dump(), creator_id=cur_user_id)
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def update_task(self, task: Task, task_data: TaskUpdate) -> Task:
        for name, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, name, value)
        await self.session.commit()
        return task

    async def del_task(self, task: Task) -> None:
        await self.session.delete(task)
        await self.session.commit()

