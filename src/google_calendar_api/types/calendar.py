from typing_extensions import NotRequired, Required, TypedDict

from ..schema.calendar import Attendee, Reminders

__all__ = ["EventParam", "ApplicationAddEventParam"]


class EventParam(TypedDict, total=False):
    summary: str | None
    start_time: str | None
    end_time: str | None
    location: str | None
    description: str | None
    attendees: list[Attendee] | None
    reminders: Reminders | None
    time_zone: str | None


class ApplicationAddEventParam(TypedDict, total=False):
    summary: Required[str]
    start_time: Required[str]
    end_time: Required[str]
    location: Required[str]
    description: Required[str | None]
    attendees: NotRequired[list[Attendee] | None]
    reminders: NotRequired[Reminders | None]
