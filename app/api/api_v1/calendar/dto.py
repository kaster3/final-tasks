from datetime import date, time
from pydantic import BaseModel

from app.core.database.models.enums.event_type import EventType


class CalendarEventBase(BaseModel):
    title: str
    description: str | None = None
    event_date: date
    start_time: time
    end_time: time
    event_type: EventType
    task_id: int | None = None
    meeting_id: int | None = None
    participants: list[int] | None = None
    company_id: int



class CalendarCreateRequest(CalendarEventBase):
    pass

class CalendarResponse(CalendarEventBase):
    id: int
    user_id: int


