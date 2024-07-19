from typing import Literal

from pydantic import BaseModel

__all__ = ["Event", "Attendee", "Reminders", "QueryEvent"]


class Creator(BaseModel):
    email: str
    self: bool


class Organizer(BaseModel):
    email: str
    self: bool


class Attendee(BaseModel):
    email: str
    responseStatus: Literal[
        "needsAction",  # 與會者尚未回覆邀請（建議用於新活動）
        "declined",  # 與會者拒絕了邀請
        "tentative",  # 與會者已暫時接受邀請
        "accepted",  # 與會者已接受邀請
    ]


class ReminderOverride(BaseModel):
    method: str
    minutes: int


class Reminders(BaseModel):
    useDefault: bool
    overrides: list[ReminderOverride] | None = None


class EventTime(BaseModel):
    dateTime: str
    timeZone: str


class EventDate(BaseModel):
    date: str  # date format : yyyy-mm-dd


class Event(BaseModel):
    kind: str
    etag: str
    id: str
    status: Literal[
        "confirmed",  # 事件已確認。這是預設狀態。
        "tentative",  # 事件已初步確認。
        "cancelled",  # 事件被取消（刪除）。
    ]
    htmlLink: str
    created: str
    updated: str
    summary: str
    visibility: (
        Literal[
            "default",  # 使用日曆上事件的預設可見性。這是預設值
            "public",  # 該活動是公開的，日曆的所有讀者都可以看到活動詳細資訊
            "private",  # 活動是私人活動，只有活動參與者才能查看活動詳細資訊
            "confidential",  # 該活動是私人活動。提供此值是出於相容性原因
        ]
        | None
    ) = None
    description: str | None = None
    location: str | None = None
    creator: Creator
    organizer: Organizer
    start: EventTime | EventDate
    end: EventTime | EventDate
    recurringEventId: str | None = None
    originalStartTime: EventTime | EventDate | None = None
    iCalUID: str
    sequence: int
    attendees: list[Attendee] = []
    reminders: Reminders
    eventType: str


class QueryEvent(BaseModel):
    kind: str
    etag: str
    summary: str
    description: str
    updated: str
    timeZone: str
    accessRole: str
    defaultReminders: list[ReminderOverride]
    nextPageToken: str | None = None
    items: list[Event] = []
