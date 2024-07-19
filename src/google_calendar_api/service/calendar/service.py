from typing import Literal

from googleapiclient.discovery import Resource
from typing_extensions import Unpack

from ...log import LOGGER
from ...schema.calendar import Event, QueryEvent
from ...types.calendar import EventParam

__all__ = ["CalendarService"]


class CalendarService:
    def __init__(self, service: Resource, calendar_id: str = "primary") -> None:
        from ...calendar import Calendar

        self.calendar = Calendar(service=service)
        self.calendar_id = calendar_id

    def get_event_date_string(self, event: Event, attr: Literal["start", "end"]) -> str:
        attr_value = getattr(event, attr)

        return getattr(attr_value, "datetime", attr_value.date)

    def process_event_to_event_param(self, event: Event) -> EventParam:
        return EventParam(
            summary=event.summary,
            start_time=self.get_event_date_string(event, "start"),
            end_time=self.get_event_date_string(event=event, attr="end"),
            location=event.location,
            description=event.description,
            attendees=event.attendees,
            reminders=event.reminders,
            time_zone=getattr(event.start, "timeZone", None),
        )

    def add_calendar_event(self, **event_param: Unpack[EventParam]) -> Event:
        if "summary" not in event_param:
            raise KeyError('"summary" key must be exists in event_param')

        LOGGER.info(msg=f"Inserting event into calendar {self.calendar_id}")

        event = self.calendar.insert_event(calendar_id=self.calendar_id, **event_param)

        LOGGER.info(
            msg=f"Event inserted: {event.id}, summary is {event_param['summary']}"
        )

        return event

    def get_calendar_event(self, event_id: str) -> Event:
        LOGGER.info(msg=f"Get {event_id} into calendar")

        return self.calendar.get_event(calendar_id=self.calendar_id, event_id=event_id)

    def get_calendar_events(
        self,
        page_token: str | None = None,
        time_min: str | None = None,
        time_max: str | None = None,
        max_results: int = 10,
        order_by: Literal["startTime", "updated"] = "startTime",
        q: str | None = None,
        single_events: bool = True,
        time_zone: str | None = None,
        show_deleted: bool = False,
    ) -> QueryEvent:
        LOGGER.info(msg=f"Get all event into {self.calendar_id}")

        return self.calendar.list_events(
            calendar_id=self.calendar_id,
            page_token=page_token,
            time_min=time_min,
            time_max=time_max,
            max_results=max_results,
            order_by=order_by,
            q=q,
            single_events=single_events,
            time_zone=time_zone,
            show_deleted=show_deleted,
        )

    def update_calendar_event(self, event_id: str, **event_param: Unpack[EventParam]):
        LOGGER.info(f"Updating event {event_id} in calendar {self.calendar_id}")

        event = self.calendar.update_event(
            calendar_id=self.calendar_id, event_id=event_id, **event_param
        )

        LOGGER.info(f"Event updated: {event.id}")

        return event

    def patch_calendar_event(
        self,
        event_id: str,
        **event_param: Unpack[EventParam],
    ) -> Event:
        LOGGER.info(f"f'Patching event {event_id} in calendar {self.calendar_id}")

        event = self.calendar.update_event(
            calendar_id=self.calendar_id, event_id=event_id, **event_param
        )

        LOGGER.info(f"Event patched: {event.id}")

        return event

    def delete_event(self, calendar_id: str, event_id: str) -> bool:
        from googleapiclient.errors import HttpError

        try:
            self.calendar.delete_event(calendar_id, event_id)
            LOGGER.info(
                f"Event {event_id} in calendar {calendar_id} deleted successfully."
            )
            return True
        except HttpError as error:
            LOGGER.error(
                f"Failed to delete event {event_id} in calendar {calendar_id}: {error}"
            )
            return False

    def move_calendar_event(
        self,
        event_id: str,
        new_start_time: str,
        new_end_time: str,
        time_zone: str | None = None,
    ) -> Event:
        LOGGER.info(
            f"Moving event {event_id} in calendar {self.calendar_id} to new times: {new_start_time} - {new_end_time}"
        )
        event = self.patch_calendar_event(
            event_id=event_id,
            start_time=new_start_time,
            end_time=new_end_time,
            time_zone=time_zone,
        )
        LOGGER.info(f"Event moved: {event.id}")

        return event
