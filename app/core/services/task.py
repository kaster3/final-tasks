from fastapi import HTTPException

from app.api.api_v1.tasks.dto import TaskCreate, TaskUpdate
from app.core.database.models import Task
from app.core.repository.interfaces.task import IDBTaskRepository
from app.core.services.user_client import UserServiceClient


class TaskService:
    def __init__(
            self,
            task_repo: IDBTaskRepository,
            user_client: UserServiceClient,
    ) -> None:
        self.task_repo = task_repo
        self.user_client = user_client

    async def get_task(self, task_id: int) -> Task | None:
        task = await self.task_repo.get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    async def create_task(self, task_data: TaskCreate, cur_user_id: int) -> Task:
        #TODO проверка на админа
        await self.user_client.get_user_by_id(user_id=task_data.assignee_id)
        await self.user_client.get_company_by_id(company_id=task_data.company_id)
        return await self.task_repo.create_task(task_data, cur_user_id=cur_user_id)

    async def update_task(self, task_id: int, task_data: TaskUpdate) -> Task:
        # TODO проверка на админа, админа компании или же сотрудник на ком эта задача
        task = await self.get_task(task_id=task_id)
        return await self.task_repo.update_task(task, task_data)

    async def del_task(self, task_id: int) -> None:
        # TODO проверка на админа, админа компании или если задача выполнена
        task = await self.get_task(task_id=task_id)
        await self.task_repo.del_task(task)


