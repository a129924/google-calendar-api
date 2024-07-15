from typing_extensions import TypedDict

from ..schema.calendar import Attendee, Reminders

__all__ = ["EventParam"]


class EventParam(TypedDict, total=False):
    summary: str | None
    start_time: str | None
    end_time: str | None
    location: str | None
    description: str | None
    attendees: list[Attendee] | None
    reminders: Reminders | None
    time_zone: str | None
