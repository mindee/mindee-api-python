from dataclasses import dataclass

from mindee.v1.error.mindee_api_error import MindeeAPIError
from mindee.v1.mindee_http.base_settings import API_KEY_ENV_NAME, BaseSettings


@dataclass
class MindeeAPI(BaseSettings):
    """Settings class relating to API requests."""

    def __init__(
        self,
        api_key: str | None,
        endpoint_name: str,
        account_name: str,
        version: str,
    ):
        super().__init__(api_key)
        if not self.api_key or len(self.api_key) == 0:
            raise MindeeAPIError(
                f"Missing API key for '{endpoint_name} v{version}' (belonging to {account_name}),"
                " check your Client configuration.\n"
                "You can set this using the "
                f"'{API_KEY_ENV_NAME}' environment variable."
            )
        self.endpoint_name = endpoint_name
        self.account_name = account_name
        self.version = version
        self.url_root = f"{self.base_url}/products/{self.account_name}/{self.endpoint_name}/v{self.version}"
