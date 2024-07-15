from typing import Literal, Unpack

from googleapiclient.discovery import Resource
from typing_extensions import Self

from ..schema.calendar import Attendee, Event, Reminders
from ..types.calendar import EventParam

__all__ = ["Calendar"]


class Calendar:
    def __init__(self, service: Resource) -> None:
        self.service = service

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc, exc_tb) -> None:
        self.service.close()

    @property
    def events(self) -> Resource:
        return self.service.events()  # type: ignore

    def _serial_event(self, **event_params: Unpack[EventParam]) -> EventParam:
        return {k: v for k, v in event_params.items() if v}  # type: ignore

    def get_event(self, calendar_id: str, event_id: str) -> Event:
        """
        get_event 取得calendar event
        doc : https://developers.google.com/calendar/api/v3/reference/events/get

        Args:
            calendar_id (str): 分享時的`calendarID`
            event_id (str): 事件的id

        Returns:
            Event: calendar event
        """
        return Event(
            **self.events.get(calendarId=calendar_id, eventId=event_id).execute()  # type: ignore
        )

    def list_events(
        self,
        calendar_id: str = "primary",
        *,
        time_min: str | None = None,
        time_max: str | None = None,
        max_results: int = 10,
        order_by: Literal["startTime", "updated"] = "startTime",
        q: str | None = None,
        single_events: bool = True,
        time_zone: str | None = None,
        show_deleted: bool = False,
    ) -> list[Event]:
        """
        list_events Read All events
        doc : https://developers.google.com/calendar/api/v3/reference/events/list

        Args:
            calendar_id (str, optional): 分享時的`calendarID` 或者是預設 `primary`. Defaults to "primary".
            time_min (str | None, optional): 時間區間起始時間 datetime string `example : 2024-07-15T09:00:00-07:00`. Defaults to None.
            time_max (str | None, optional): 時間區間結束時間 datetime string `example : 2024-07-16T09:00:00-07:00`. Defaults to None.
            max_results (int, optional): 最大的回傳數. Defaults to 10.
            order_by (Literal[&quot;startTime&quot;, &quot;updated&quot;], optional): 排序方式 由開始時間(startTime)或者更新時間(updated). Defaults to "startTime".
            q (str | None, optional): 搜尋關鍵字. Defaults to None.
            single_events (bool, optional): 如果為True，將重複事件展平為單個事件. Defaults to True.
            time_zone (str | None, optional): 時區，返回的事件時間將根據此時區調整. Defaults to None.
            show_deleted (bool, optional): 如果為True，則包括已刪除的事件. Defaults to False.

        Returns:
            dict[str, Any]: 包含事件列表的字典
        """
        return [
            Event(**event)
            for event in self.events.list(  # type: ignore
                calendar_id=calendar_id,
                time_min=time_min,
                time_max=time_max,
                max_results=max_results,
                order_by=order_by,
                q=q,
                single_events=single_events,
                time_zone=time_zone,
                show_deleted=show_deleted,
            ).execute()
        ]

    def update_event(
        self,
        calendar_id: str,
        event_id: str,
        *,
        summary: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        location: str | None = None,
        description: str | None = None,
        attendees: list[Attendee] | None = None,
        reminders: Reminders | None = None,
        time_zone: str | None = None,
    ) -> Event:
        """
        update_event 用於更新整個事件。它需要傳遞完整的事件對象。如果事件對象中缺少某些字段，這些字段將被設置為其默認值。
        doc : `https://developers.google.com/calendar/api/v3/reference/events/update`

        Args:
            calendar_id (str): 分享時的`calendarID`
            event_id (str): 事件的id
            summary (str | None, optional): 預修改的摘要. Defaults to None.
            start_time (str | None, optional): 預修改的起始時間. Defaults to None.
            end_time (str | None, optional): 預修改的起始時間. Defaults to None.
            location (str | None, optional): 預修改的結束時間. Defaults to None.
            description (str | None, optional): 預修改的內容. Defaults to None.
            attendees (list[Attendee] | None, optional): 預修改的參加者. Defaults to None.
            reminders (Reminders | None, optional): 預修改的提醒. Defaults to None.
            time_zone (str, optional): 預修改的時區. Defaults to None.

        Returns:
            Event: 回傳已修改的事件
        """
        event: Event = self.get_event(calendar_id=calendar_id, event_id=event_id)

        update_event = event.model_copy(
            update=self._serial_event(
                summary=summary,
                start_time=start_time,
                end_time=end_time,
                location=location,
                description=description,
                attendees=attendees,
                reminders=reminders,
                time_zone=time_zone,
            )  # type: ignore
        )

        return Event(
            **self.events.update(  # type: ignore
                calendarId=calendar_id,
                eventId=event_id,
                body=update_event.model_dump(),
            )
        )

    def patch_event(
        self,
        calendar_id: str,
        event_id: str,
        *,
        summary: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        location: str | None = None,
        description: str | None = None,
        attendees: list[Attendee] | None = None,
        reminders: Reminders | None = None,
        time_zone: str | None = None,
    ) -> Event:
        """
        update_event 用於部分更新事件。它僅更新事件對象中指定的字段，而不會改變未指定的字段
        doc : `https://developers.google.com/calendar/api/v3/reference/events/patch`

        Args:
            calendar_id (str): 分享時的`calendarID`
            event_id (str): 事件的id
            summary (str | None, optional): 預修改的摘要. Defaults to None.
            start_time (str | None, optional): 預修改的起始時間. Defaults to None.
            end_time (str | None, optional): 預修改的起始時間. Defaults to None.
            location (str | None, optional): 預修改的結束時間. Defaults to None.
            description (str | None, optional): 預修改的內容. Defaults to None.
            attendees (list[Attendee] | None, optional): 預修改的參加者. Defaults to None.
            reminders (Reminders | None, optional): 預修改的提醒. Defaults to None.
            time_zone (str, optional): 預修改的時區. Defaults to None.

        Returns:
            Event: 回傳已修改的事件
        """
        return Event(
            **self.events.patch(  # type: ignore
                calendarId=calendar_id,
                eventId=event_id,
                body=self._serial_event(
                    summary=summary,
                    start_time=start_time,
                    end_time=end_time,
                    location=location,
                    description=description,
                    attendees=attendees,
                    reminders=reminders,
                    time_zone=time_zone,
                ),
            )
        )

    def insert_event(
        self,
        calendar_id: str,
        *,
        summary: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        location: str | None = None,
        description: str | None = None,
        attendees: list[Attendee] | None = None,
        reminders: Reminders | None = None,
        time_zone: str | None = None,
    ) -> Event:
        """
        insert_event add new event
        doc : https://developers.google.com/calendar/api/v3/reference/events/insert

        Args:
            calendar_id (str): 分享時的`calendarID`
            summary (str | None, optional): 預計新增的摘要. Defaults to None.
            start_time (str | None, optional): 預計新增的起始時間. Defaults to None.
            end_time (str | None, optional): 預計新增的起始時間. Defaults to None.
            location (str | None, optional): 預計新增的結束時間. Defaults to None.
            description (str | None, optional): 預計新增的內容. Defaults to None.
            attendees (list[Attendee] | None, optional): 預計新增的參加者. Defaults to None.
            reminders (Reminders | None, optional): 預計新增的提醒. Defaults to None.
            time_zone (str, optional): 預計新增的時區. Defaults to None.

        Returns:
            Event: 已新增的事件
        """
        return Event(
            **self.events.insert(  # type: ignore
                calendarId=calendar_id,
                body=self._serial_event(
                    summary=summary,
                    start_time=start_time,
                    end_time=end_time,
                    location=location,
                    description=description,
                    attendees=attendees,
                    reminders=reminders,
                    time_zone=time_zone,
                ),
            )
        )

    def delete_event(self, calendar_id: str, event_id: str) -> bool:
        from googleapiclient.errors import HttpError

        """
        delete_event 刪除事件
        doc : https://developers.google.com/calendar/api/v3/reference/events/delete

        Args:
            calendar_id (str): 分享時的`calendarID`
            event_id (str): 預計刪除的事件ID

        Returns:
            bool : 回傳是否刪除
        """
        try:
            self.events.delete(calendarId=calendar_id, eventId=event_id).execute()  # type: ignore

            return True
        except HttpError:
            return False
