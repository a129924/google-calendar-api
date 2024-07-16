from googleapiclient.discovery import Resource

from ...credentials import Credentials


class CredentialsService:
    def __init__(self, credentials: Credentials, token_json_path: str | None = None):
        self.credentials = credentials
        self.token_json_path = token_json_path

    def get_service(self, service_name: str, version: str) -> Resource:
        if self.credentials.need_refresh():
            self.credentials.refresh_token()

            if self.token_json_path:
                self.to_json_file(self.token_json_path)

        return self.credentials.build_service(service_name, version)

    def to_json_file(self, token_json_path: str) -> None:
        self.credentials.to_json_file(token_json_path=token_json_path)

    @staticmethod
    def from_token_params(
        token: str,
        refresh_token: str,
        token_uri: str,
        client_id: str,
        client_secret: str,
        scopes: list[str],
    ) -> "CredentialsService":
        creds = Credentials(
            token=token,
            refresh_token=refresh_token,
            token_uri=token_uri,
            client_id=client_id,
            client_secret=client_secret,
            scopes=scopes,
        ).create_credentials()

        return CredentialsService(creds)

    @staticmethod
    def from_client_secrets_file(
        credentials_json_path: str,
        scopes: list[str],
        port: int = 0,
        *,
        output_token_json: str,
    ) -> "CredentialsService":
        creds = Credentials.from_client_secrets_file(
            credentials_json_path, scopes, port
        )

        return CredentialsService(creds, token_json_path=output_token_json)

    @staticmethod
    def from_authorized_user_file(
        token_json_path: str, scopes: list[str]
    ) -> "CredentialsService":
        creds = Credentials.from_authorized_user_file(token_json_path, scopes)

        return CredentialsService(creds, token_json_path)
