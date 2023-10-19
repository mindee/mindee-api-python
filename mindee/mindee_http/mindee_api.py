import os
from dataclasses import dataclass
from typing import Dict, Optional, Union

from mindee.error.mindee_error import MindeeApiError
from mindee.logger import logger
from mindee.versions import __version__, get_platform, python_version

API_KEY_ENV_NAME = "MINDEE_API_KEY"
API_KEY_DEFAULT = ""

BASE_URL_ENV_NAME = "MINDEE_BASE_URL"
BASE_URL_DEFAULT = "https://api.mindee.net/v1"

REQUEST_TIMEOUT_ENV_NAME = "MINDEE_REQUEST_TIMEOUT"
TIMEOUT_DEFAULT = 120

PLATFORM = get_platform()
USER_AGENT = f"mindee-api-python@v{__version__} python-v{python_version} {PLATFORM}"


@dataclass
class MindeeApi:
    """Settings class relating to API requests."""

    api_key: Optional[str]
    """API Key for the client."""
    base_url: str
    request_timeout: int

    def __init__(
        self,
        api_key: Optional[str],
        endpoint_name: str,
        account_name: str,
        version: str,
    ):
        self._set_api_key(api_key)
        if not self.api_key or len(self.api_key) == 0:
            raise MindeeApiError(
                (
                    f"Missing API key for '{endpoint_name} v{version}' (belonging to {account_name}),"
                    " check your Client configuration.\n"
                    "You can set this using the "
                    f"'{API_KEY_ENV_NAME}' environment variable."
                )
            )
        self.endpoint_name = endpoint_name
        self.account_name = account_name
        self.version = version
        self.request_timeout = TIMEOUT_DEFAULT
        self.set_base_url(BASE_URL_DEFAULT)
        self.set_from_env()
        self.url_root = f"{self.base_url}/products/{self.account_name}/{self.endpoint_name}/v{self.version}"

    @property
    def base_headers(self) -> Dict[str, str]:
        """Base headers to send with all API requests."""
        return {
            "Authorization": f"Token {self.api_key}",
            "User-Agent": USER_AGENT,
        }

    def _set_api_key(self, api_key: Optional[str]) -> None:
        """Set the endpoint's API key from an environment variable, if present."""
        env_val = os.getenv(API_KEY_ENV_NAME, "")
        if env_val and (not api_key or len(api_key) == 0):
            logger.debug("API key set from environment")
            self.api_key = env_val
            return
        self.api_key = api_key

    def set_from_env(self) -> None:
        """Set various parameters from environment variables, if present."""
        env_vars = {
            BASE_URL_ENV_NAME: self.set_base_url,
            REQUEST_TIMEOUT_ENV_NAME: self.set_timeout,
        }
        for name, func in env_vars.items():
            env_val = os.getenv(name, "")
            if env_val:
                func(env_val)
                logger.debug("Value was set from env: %s", name)

    def set_timeout(self, value: Union[str, int]) -> None:
        """Set the timeout for all requests."""
        self.request_timeout = int(value)

    def set_base_url(self, value: str) -> None:
        """Set the base URL for all requests."""
        self.base_url = value
