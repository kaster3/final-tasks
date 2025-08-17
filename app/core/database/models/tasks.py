from sqlalchemy import Text, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.models.base import Base
from app.core.database.models.enums.task_status import TaskStatus
from app.core.database.models.mixins.pk_id_mixin import IntIdPkMixin


class Task(Base, IntIdPkMixin):
    title: Mapped[str] = mapped_column(String(length=100))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.TODO)
    creator_id: Mapped[str] = mapped_column(comment="ID юзера из User Service, кто назначает задачу")
    assignee_id: Mapped[str] = mapped_column(comment="ID юзера из User Service, которому назначают задачу")
    company_id: Mapped[str] = mapped_column(comment="ID компании из User Service")