from collections.abc import Generator
from typing import Literal

from googleapiclient.discovery import Resource
from typing_extensions import Unpack

from .config import CalendarConfig
from .log import LOGGER
from .schema.calendar import Event
from .service.calendar import CalendarService
from .service.credentials import CredentialsService
from .types.calendar import ApplicationAddEventParam


class GoogleCalendarAPI:
    def __init__(
        self,
        token: str | None = None,
        refresh_token: str | None = None,
        token_uri: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        scopes: list[str] | None = None,
        token_json_path: str | None = None,
        credentials_json_path: str | None = None,
        port: int = 0,
        *,
        calendar_config_path: str,
    ) -> None:
        if (
            token
            and refresh_token
            and token_uri
            and client_id
            and client_secret
            and scopes
        ):
            self.service = self._load_from_token_params(
                token,
                refresh_token,
                token_uri,
                client_id,
                client_secret,
                scopes,
            )
        elif token_json_path and scopes:
            self.service = self._load_from_token_json(token_json_path, scopes)
        elif credentials_json_path and port and scopes and token_json_path:
            self.service = self._load_from_credentials_json(
                credentials_json_path, scopes, port, token_json_path
            )
        else:
            LOGGER.error("Invalid initialization parameters for GoogleCalendarAPI")
            raise ValueError("Invalid initialization parameters for GoogleCalendarAPI")

        config = CalendarConfig.set_model_config(
            {"json_file": calendar_config_path, "json_file_encoding": "UTF-8"}
        )()  # type: ignore

        self.calendar_service = CalendarService(
            service=self.service, calendar_id=config.calendar_id
        )
        self.time_zone = config.time_zone

    @staticmethod
    def _load_from_token_params(
        token: str,
        refresh_token: str,
        token_uri: str,
        client_id: str,
        client_secret: str,
        scopes: list[str],
    ) -> Resource:
        return CredentialsService.from_token_params(
            token=token,
            refresh_token=refresh_token,
            token_uri=token_uri,
            client_id=client_id,
            client_secret=client_secret,
            scopes=scopes,
        ).get_service("calendar", "v3")

    @staticmethod
    def _load_from_token_json(token_json_path: str, scopes: list[str]) -> Resource:
        return CredentialsService.from_authorized_user_file(
            token_json_path=token_json_path, scopes=scopes
        ).get_service("calendar", "v3")

    @staticmethod
    def _load_from_credentials_json(
        credentials_json_path: str,
        scopes: list[str],
        port: int,
        output_token_json: str,
    ) -> Resource:
        return CredentialsService.from_client_secrets_file(
            credentials_json_path=credentials_json_path,
            scopes=scopes,
            port=port,
            output_token_json=output_token_json,
        ).get_service("calendar", "v3")

    def replace_calendar_event(
        self,
        event_or_event_id: Event | str,
        **event_param: Unpack[ApplicationAddEventParam],
    ) -> Event:
        if isinstance(event_or_event_id, str):
            event = self.get_calendar_event(event_id=event_or_event_id)

        replace_event = event.model_copy(update=event_param)  # type: ignore

        return self.calendar_service.update_calendar_event(
            event_id=replace_event.id,
            **self.calendar_service.process_event_to_event_param(event=replace_event),
        )

    def get_calendar_event(self, event_id: str) -> Event:
        return self.calendar_service.get_calendar_event(event_id)

    def get_calendar_events(
        self,
        *,
        time_min: str,
        time_max: str,
        max_results: int = 10,
        order_by: Literal["startTime", "updated"] = "startTime",
        q: str | None = None,
    ) -> Generator[Event, None, None]:
        page_token: str | None = None

        while True:
            query_event = self.calendar_service.get_calendar_events(
                time_min=time_min,
                time_max=time_max,
                page_token=page_token,
                max_results=max_results,
                order_by=order_by,
                q=q,
                time_zone=self.time_zone,
            )

            if page_token := query_event.nextPageToken:
                yield from query_event.items
            else:
                break

    def add_calendar_event(
        self, replace: bool = False, **event_param: Unpack[ApplicationAddEventParam]
    ) -> Event | None:
        if replace:
            try:
                return self.replace_calendar_event(
                    event_or_event_id=self.get_calendar_events(
                        time_min=event_param["start_time"],
                        time_max=event_param["end_time"],
                        q=event_param["summary"],
                    ).__next__(),
                    **event_param,
                )
            except StopIteration:
                return None
        else:
            return self.calendar_service.add_calendar_event(
                time_zone=self.time_zone, **event_param
            )
