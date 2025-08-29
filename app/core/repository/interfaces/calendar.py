from abc import abstractmethod
from datetime import date, time
from typing import Protocol

from app.api.api_v1.calendar.dto import CalendarCreateRequest
from app.core.database.models.calendar import CalendarEvent


class IDBCalendarRepository(Protocol):
    @abstractmethod
    async def get_user_events(
            self,
            cur_user_id: int,
            start_date: date,
            end_date: date,
    ) -> list[CalendarEvent]:
        raise NotImplementedError

    @abstractmethod
    async def create_event(
            self,
            event_data: CalendarCreateRequest,
            user_id: int,
    ) -> CalendarEvent:
        raise NotImplementedError

    @abstractmethod
    async def check_time_availability(
            self,
            user_id: int,
            event_date: date,
            start_time: time,
            end_time: time,
            exclude_event_id: int | None = None
    ) -> bool:
        raise NotImplementedError

