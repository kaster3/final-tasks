from datetime import date, time

from pydantic import BaseModel, Field


class MeetingBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Название встречи")
    description: str | None = Field(None, max_length=1000, description="Описание встречи")
    event_date: date = Field(..., description="Дата встречи")
    start_time: time = Field(..., description="Время начала встречи")
    end_time: time = Field(..., description="Время окончания встречи")
    company_id: int = Field(..., gt=0, description="ID компании")
    participant_ids: list[int] = Field(..., description="Список ID участников")

class MeetingCreateRequest(MeetingBase):
    pass

class MeetingUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200, description="Название встречи")
    description: str | None = Field(None, max_length=1000, description="Описание встречи")
    event_date: date | None = Field(None, description="Дата встречи")
    start_time: time | None = Field(None, description="Время начала встречи")
    end_time: time | None = Field(None, description="Время окончания встречи")
    participant_ids: list[int] | None = Field(None, description="Список ID участников")

class MeetingRead(MeetingBase):
    id: int = Field(..., description="ID встречи")
    organizer_id: int = Field(..., description="ID организатора встречи")