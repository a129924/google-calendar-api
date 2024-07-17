from .base import JsonBaseSettings


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
