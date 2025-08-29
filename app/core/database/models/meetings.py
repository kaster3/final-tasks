from datetime import date, time
from typing import TYPE_CHECKING
from sqlalchemy import String, ARRAY, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Date, Time

from app.core.database.models.base import Base
from app.core.database.models.mixins.pk_id_mixin import IntIdPkMixin

if TYPE_CHECKING:
    from app.core.database.models.calendar import CalendarEvent


class Meeting(Base, IntIdPkMixin):
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(length=1000), nullable=True)
    event_date: Mapped[date] = mapped_column(Date, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    organizer_id: Mapped[int] = mapped_column(nullable=False)
    company_id: Mapped[int] = mapped_column(nullable=False)
    participant_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer), default=list)

    # Связь с календарными событиями
    calendar_events: Mapped[list["CalendarEvent"]] = relationship(
        "CalendarEvent",
        back_populates="meeting",
        cascade="all, delete-orphan"
    )