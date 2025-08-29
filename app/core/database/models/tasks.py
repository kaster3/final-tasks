from typing import TYPE_CHECKING

from sqlalchemy import Text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.models.base import Base
from app.core.database.models.enums.task_status import TaskStatus
from app.core.database.models.mixins.pk_id_mixin import IntIdPkMixin

if TYPE_CHECKING:
    from app.core.database.models import TaskComment
    from app.core.database.models import CalendarEvent


class Task(Base, IntIdPkMixin):
    title: Mapped[str] = mapped_column(String(length=100))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.TODO)
    creator_id: Mapped[int] = mapped_column(comment="ID юзера из User Service, кто назначает задачу")
    assignee_id: Mapped[int] = mapped_column(comment="ID юзера из User Service, которому назначают задачу")
    company_id: Mapped[int] = mapped_column(comment="ID компании из User Service")

    # Связи
    comments: Mapped[list["TaskComment"]] = relationship(
        back_populates="task",
        cascade="all, delete-orphan",
        order_by="TaskComment.created_at.desc()"
    )
    calendar_events: Mapped[list["CalendarEvent"]] = relationship(
        "CalendarEvent",
        back_populates="task",
        cascade="all, delete-orphan"
    )