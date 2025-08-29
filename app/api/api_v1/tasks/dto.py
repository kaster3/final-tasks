from pydantic import BaseModel, Field

from app.core.database.models.enums.task_status import TaskStatus


class TaskBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: str = Field(...)
    status: TaskStatus
    assignee_id: int
    company_id: int

class TaskRead(TaskBase):
    id: int

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskRead):
    pass