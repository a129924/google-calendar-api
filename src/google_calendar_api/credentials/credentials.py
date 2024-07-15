from google.auth import credentials
from googleapiclient.discovery import Resource
from typing_extensions import Self

__all__ = ["Credentials"]


class Credentials:
    def __init__(
        self,
        token: str | None = None,
        refresh_token: str | None = None,
        token_uri: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        scopes: list[str] | None = None,
        universe_domain: str = credentials.DEFAULT_UNIVERSE_DOMAIN,
        account: str | None = None,
        expiry: str | None = None,
    ) -> None:
        self.token = token
        self._refresh_token = refresh_token
        self.token_uri = token_uri
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes
        self.universe_domain = universe_domain
        self.account = account
        self.expiry = expiry

    def create_credentials(
        self,
    ) -> Self:
        from google.oauth2.credentials import Credentials

        self.credential = Credentials(
            token=self.token,
            refresh_token=self._refresh_token,
            token_uri=self.token_uri,
            client_id=self.client_id,
            client_secret=self.client_secret,
            scopes=self.scopes,
            universe_domain=self.universe_domain,
            account=self.account,
            expiry=self.expiry,
        )

        return self

    def refresh_token(self) -> Self:
        from google.auth.transport.requests import Request

        self.credential.refresh(Request())

        return self

    @classmethod
    def token_from_client_secrets_file(
        cls,
        credentials_json_path: str,
        scopes: list[str],
        port: int = 0,
    ) -> "Credentials":
        from os.path import exists

        if exists(credentials_json_path):
            from google_auth_oauthlib.flow import InstalledAppFlow

            cls.credential = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file=credentials_json_path, scopes=scopes
            ).run_local_server(port=port)

            return cls()

        raise FileNotFoundError(f"{credentials_json_path} is not exist")

    def need_refresh(self) -> bool:
        return self.credential.valid and self.credential.expired and self.refresh_token

    @classmethod
    def from_authorized_user_file(
        cls, token_json_path: str, scopes: list[str]
    ) -> "Credentials":
        from os.path import exists

        if exists(token_json_path):
            from google.oauth2.credentials import Credentials

            cls.credential = Credentials.from_authorized_user_file(
                filename=token_json_path, scopes=scopes
            )

            return cls()

        raise FileNotFoundError(f"{token_json_path} is not exist")

    def build_service(self, service_name: str, version: str) -> Resource:
        from googleapiclient.discovery import build

        return build(serviceName=service_name, version=version)
