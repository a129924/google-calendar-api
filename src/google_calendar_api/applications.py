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

        self.calendar = CalendarService(
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
        self, events: list[Event], **event_param: Unpack[ApplicationAddEventParam]
    ) -> Event | None:
        if events:
            replace_event = events[0].model_copy(update=event_param)  # type: ignore

            return self.calendar.update_calendar_event(
                event_id=replace_event.id,
                **self.calendar.process_event_to_event_param(event=replace_event),
            )

        else:
            return None

    def add_calendar_event(
        self, replace: bool = False, **event_param: Unpack[ApplicationAddEventParam]
    ) -> Event | None:
        if replace:
            query_events = self.calendar.get_calendar_events(
                time_min=event_param["start_time"],
                time_max=event_param["end_time"],
                q=event_param["summary"],
                time_zone=self.time_zone,
            )

            return self.replace_calendar_event(events=query_events, **event_param)
        else:
            return self.calendar.add_calendar_event(
                time_zone=self.time_zone, **event_param
            )
        ...
