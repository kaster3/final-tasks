from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.models import Meeting
from app.core.repository.interfaces.meeting import IDBMeetingRepository
from app.api.api_v1.meetings.dto import MeetingCreateRequest, MeetingUpdate


class SQLAlchemyMeetingRepository(IDBMeetingRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, meeting_id: int) -> Meeting | None:
        meeting = await self.session.get(Meeting, meeting_id)
        return meeting

    async def create(self, meeting_data: MeetingCreateRequest) -> Meeting:
        meeting = Meeting(**meeting_data.model_dump())
        self.session.add(meeting)
        await self.session.commit()
        await self.session.refresh(meeting)
        return meeting

    async def update(self, meeting: Meeting, meeting_data: MeetingUpdate) -> Meeting:
        for name, value in meeting_data.model_dump(exclude_unset=True).items():
            setattr(meeting, name, value)
        await self.session.commit()
        return meeting


    async def delete(self, meeting: Meeting) -> None:
        await self.session.delete(meeting)
        await self.session.commit()