from datetime import date

from fastapi import HTTPException, status

from app.api.api_v1.calendar.dto import CalendarCreateRequest
from app.core.database.models.calendar import CalendarEvent
from app.core.database.models.enums.event_type import EventType
from app.core.repository.interfaces.calendar import IDBCalendarRepository
from app.core.services.task import TaskService
from app.core.services.user_client import UserServiceClient


class CalendarService:
    def __init__(
            self,
            task_service: TaskService,
            user_client: UserServiceClient,
            calendar_repo: IDBCalendarRepository,
    ) -> None:
        self.task_service = task_service
        self.user_client = user_client
        self.calendar_repo = calendar_repo

    async def get_user_events(
        self,
        cur_user_id: int,
        start_date: date,
        end_date: date,
    ) -> list[CalendarEvent]:
        return await self.calendar_repo.get_user_events(
            cur_user_id=cur_user_id,
            start_date=start_date,
            end_date=end_date,
        )

    async def create_event(
            self,
            event_data: CalendarCreateRequest,
    ) -> CalendarEvent:

        if event_data.event_type == EventType.TASK.value and event_data.task_id:
            task = await self.task_service.get_task(task_id=event_data.task_id)

            is_available = await self.calendar_repo.check_time_availability(
                user_id=task.assignee_id,
                event_date=event_data.event_date,
                start_time=event_data.start_time,
                end_time=event_data.end_time
            )

            if not is_available:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Time is not available",
                )

            await self.user_client.get_company_by_id(company_id=event_data.company_id)
            return await self.calendar_repo.create_event(
                user_id=task.assignee_id,
                event_data=event_data,
            )

        elif (
                event_data.event_type == EventType.MEETING.value
                and event_data.meeting_id
                and len(event_data.participants) > 1
        ):
            print("2222222-------2222222")




