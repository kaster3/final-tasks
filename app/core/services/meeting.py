from fastapi import HTTPException
from starlette import status

from app.api.api_v1.calendar.dto import CalendarCreateRequest
from app.api.api_v1.meetings.dto import MeetingCreateRequest, MeetingUpdate
from app.core.database.models import Meeting
from app.core.database.models.enums.event_type import EventType
from app.core.repository.interfaces.calendar import IDBCalendarRepository
from app.core.repository.interfaces.meeting import IDBMeetingRepository
from app.core.services.user_client import UserServiceClient


class MeetingService:
    def __init__(
            self,
            user_client: UserServiceClient,
            meeting_repo: IDBMeetingRepository,
            calendar_repo: IDBCalendarRepository,
    ) -> None:
        self.calendar_repo = calendar_repo
        self.user_client = user_client
        self.meeting_repo = meeting_repo

    async def get_meeting(self, meeting_id: int) -> Meeting | None:
        meeting = await self.meeting_repo.get_by_id(meeting_id=meeting_id)
        if not meeting:
            raise HTTPException(status_code=404, detail=f"Meeting #{meeting_id} not found")
        return meeting

    async def create_meeting(self, meeting_data: MeetingCreateRequest) -> Meeting:
        await self.user_client.get_company_by_id(company_id=meeting_data.company_id)
        for participant in meeting_data.participant_ids:
            await self.user_client.get_user_by_id(user_id=participant)

        for participant_id in meeting_data.participant_ids:
            is_available = await self.calendar_repo.check_time_availability(
                user_id=participant_id,
                event_date=meeting_data.event_date,
                start_time=meeting_data.start_time,
                end_time=meeting_data.end_time
            )

            if not is_available:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"User {participant_id} is not available at this time"
                )

        meeting = await self.meeting_repo.create(meeting_data=meeting_data)

        for participant_id in meeting_data.participant_ids:
            calendar_event_data = CalendarCreateRequest(
                title=meeting_data.title,
                description=meeting_data.description,
                event_date=meeting_data.event_date,
                start_time=meeting_data.start_time,
                end_time=meeting_data.end_time,
                event_type=EventType.MEETING,
                meeting_id=meeting.id,
                company_id=meeting_data.company_id
            )

            await self.calendar_repo.create_event(
                event_data=calendar_event_data,
                user_id=participant_id
            )

        return meeting


    async def update_meeting(
            self,
            meeting_id: int,
            meeting_data: MeetingUpdate,
    ) -> Meeting:
        pass

    async def delete_meeting(self, meeting_id: int) -> None:
        meeting = await self.get_meeting(meeting_id=meeting_id)
        await self.meeting_repo.delete(meeting=meeting)