from datetime import date, time

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api_v1.calendar.dto import CalendarCreateRequest
from app.core.database.models.calendar import CalendarEvent
from app.core.repository.interfaces.calendar import IDBCalendarRepository


class SQLAlchemyCalendarRepository(IDBCalendarRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user_events(
            self,
            cur_user_id: int,
            start_date: date,
            end_date: date,
    ) -> list[CalendarEvent]:
        stmt = (
            select(CalendarEvent)
            .where(
                and_(
                    CalendarEvent.user_id == cur_user_id,
                    CalendarEvent.event_date >= start_date,
                    CalendarEvent.event_date <= end_date
                )
            )
            .order_by(CalendarEvent.event_date, CalendarEvent.start_time)
        )

        result = await self.session.scalars(stmt)
        return list(result)


    async def create_event(
            self,
            event_data: CalendarCreateRequest,
            user_id: int,
    ) -> CalendarEvent:
        event = CalendarEvent(**event_data.model_dump(exclude_none=True), user_id=user_id)
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def check_time_availability(
            self,
            user_id: int,
            event_date: date,
            start_time: time,
            end_time: time,
            exclude_event_id: int | None = None
    ) -> bool:
        # Условия: тот же пользователь, та же дата, и пересечение времени
        conditions = [
            CalendarEvent.user_id == user_id,
            CalendarEvent.event_date == event_date,
            # Упрощенная проверка пересечения временных интервалов:
            # Новое событие НЕ должно начинаться после существующего И
            # Новое событие НЕ должно заканчиваться до существующего
            CalendarEvent.start_time < end_time,
            CalendarEvent.end_time > start_time
        ]

        # Исключаем текущее событие при редактировании
        if exclude_event_id:
            conditions.append(CalendarEvent.id != exclude_event_id)

        stmt = select(CalendarEvent).where(and_(*conditions))
        conflicting_event = await self.session.scalar(stmt)

        return conflicting_event is None



