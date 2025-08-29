from abc import abstractmethod
from typing import Protocol

from app.api.api_v1.meetings.dto import MeetingCreateRequest, MeetingUpdate
from app.core.database.models import Meeting


class IDBMeetingRepository(Protocol):
    @abstractmethod
    async def get_by_id(self, meeting_id: int) -> Meeting | None:
        raise NotImplementedError

    async def create(self, meeting_data: MeetingCreateRequest) -> Meeting:
        raise NotImplementedError

    async def update(self, meeting: Meeting, meeting_data: MeetingUpdate) -> Meeting:
        raise NotImplementedError

    async def delete(self, meeting: Meeting) -> None:
        raise NotImplementedError