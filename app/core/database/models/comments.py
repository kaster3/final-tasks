from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.models import Task
from app.core.database.models.base import Base
from app.core.database.models.mixins.pk_id_mixin import IntIdPkMixin
from app.core.database.models.mixins.timestamp_mixin import TimestampMixin

if TYPE_CHECKING:
    from app.core.database.models import Task


class TaskComment(Base, IntIdPkMixin, TimestampMixin):
    text: Mapped[str] = mapped_column(Text, nullable=False)
    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID задачи, к которой относится комментарий"
    )
    author_id: Mapped[int] = mapped_column(
        nullable=False,
        comment="ID автора комментария из User Service (JWT token)"
    )

    # Связи
    task: Mapped["Task"] = relationship(back_populates="comments")