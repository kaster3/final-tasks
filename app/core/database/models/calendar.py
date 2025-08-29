from datetime import date, time
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Date, Time

from app.core.database.models.enums.event_type import EventType
from app.core.database.models.mixins.pk_id_mixin import IntIdPkMixin
from app.core.database.models.base import Base

if TYPE_CHECKING:
    from app.core.database.models import Task
    from app.core.database.models.meetings import Meeting


class CalendarEvent(Base, IntIdPkMixin):
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(length=1000), nullable=True)
    event_date: Mapped[date] = mapped_column(Date, nullable=False)  # Дата события
    start_time: Mapped[time] = mapped_column(Time, nullable=False)  # Время начала
    end_time: Mapped[time] = mapped_column(Time, nullable=False)  # Время окончания
    event_type: Mapped[EventType] = mapped_column(nullable=False)

    # Связи
    task_id: Mapped[int | None] = mapped_column(
        ForeignKey("tasks.id"), nullable=True
    )
    meeting_id: Mapped[int | None] = mapped_column(
        ForeignKey("meetings.id"), nullable=True
    )
    user_id: Mapped[int] = mapped_column(nullable=False)
    company_id: Mapped[int] = mapped_column(nullable=False)

    # Relationships
    task: Mapped["Task"] = relationship("Task", back_populates="calendar_events")
    meeting: Mapped["Meeting"] = relationship("Meeting", back_populates="calendar_events")
