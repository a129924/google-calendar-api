from pydantic import BaseModel

from .base import JsonBaseSettings

__all__ = ["CalendarConfig"]


class Installed(BaseModel):
    client_id: str
    project_id: str
    auth_uri: str
    token_uri: str
    auth_provider_x509_cert_url: str
    client_secret: str
    redirect_uris: list[str]


class Credentials(JsonBaseSettings):
    installed: Installed


class AuthorizedUserToken(JsonBaseSettings):
    token: str
    refresh_token: str
    token_uri: str
    client_id: str
    client_secret: str
    scopes: list[str]
    universe_domain: str
    account: str
    expiry: str


class CalendarConfig(JsonBaseSettings):
    calendar_id: str
    time_zone: str
