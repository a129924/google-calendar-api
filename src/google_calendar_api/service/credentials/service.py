from googleapiclient.discovery import Resource

from ...credentials import Credentials


class CredentialsService:
    def __init__(self, credentials: Credentials, token_json_path: str | None = None):
        self.credentials = credentials
        self.token_json_path = token_json_path

    def get_service(self, service_name: str, version: str) -> Resource:
        """
        get_service 返回指定的 Google API 服務對象，並在需要時刷新憑證。

        Args:
            service_name (str): Google API 服務的名稱（例如 "calendar"）。
            version (str): Google API 服務的版本（例如 "v3"）。

        Returns:
            CredentialService: 指定的 Google API 服務對象。
        """
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
        """
        from_token_params 從提供的 token 參數生成 CredentialService 實例。

        Args:
            token (str): 訪問 token。
            refresh_token (str): 刷新 token。
            token_uri (str): token URI。
            client_id (str): 客戶端 ID。
            client_secret (str): 客戶端密鑰。
            scopes (list[str]): 授權範圍。

        Returns:
            CredentialsService: 生成的 CredentialService 實例。
        """
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
        """
        from_client_secrets_file 產生google service 必要的client secrets file

        Args:
            credentials_json_path (str): client secrets filepath
            scopes (list[str]): 服務網址
            output_token_json (str): 憑證刷新後將新的憑證保存到這個路徑（如果提供）。
            port (int, optional): port號. Defaults to 0.

        Returns:
            CredentialsService: 生成的 CredentialService 實例。
        """
        creds = Credentials.from_client_secrets_file(
            credentials_json_path, scopes, port
        )

        return CredentialsService(creds, token_json_path=output_token_json)

    @staticmethod
    def from_authorized_user_file(
        token_json_path: str, scopes: list[str]
    ) -> "CredentialsService":
        """
        from_authorized_user_file 產生google service 必要的token path

        Args:
            token_json_path (str): 憑證刷新後將新的憑證保存到這個路徑（如果提供）。
            scopes (list[str]): 服務網址

        Returns:
            CredentialsService: 生成的 CredentialService 實例。
        """
        creds = Credentials.from_authorized_user_file(token_json_path, scopes)

        return CredentialsService(creds, token_json_path)
