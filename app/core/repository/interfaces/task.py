from abc import abstractmethod
from typing import Protocol

from app.api.api_v1.tasks.dto import TaskCreate, TaskUpdate
from app.core.database.models import Task


class IDBTaskRepository(Protocol):
    @abstractmethod
    async def get_task(self, task_id: int) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    async def create_task(self, task_data: TaskCreate, cur_user_id: int) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def update_task(self, task: Task, task_data: TaskUpdate) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def del_task(self, task: Task) -> None:
        raise NotImplementedError
