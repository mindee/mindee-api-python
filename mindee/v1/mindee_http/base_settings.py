import os
from dataclasses import dataclass
from typing import Dict, Optional

from mindee.logger import logger
from mindee.mindee_http.settings_mixin import SettingsMixin
from mindee.versions import PYTHON_VERSION, __version__, get_platform

API_KEY_ENV_NAME = "MINDEE_API_KEY"
API_KEY_DEFAULT = ""

BASE_URL_ENV_NAME = "MINDEE_BASE_URL"
BASE_URL_DEFAULT = "https://api.mindee.net/v1"

REQUEST_TIMEOUT_ENV_NAME = "MINDEE_REQUEST_TIMEOUT"
TIMEOUT_DEFAULT = 120

PLATFORM = get_platform()
USER_AGENT = f"mindee-api-python@v{__version__} python-v{PYTHON_VERSION} {PLATFORM}"


@dataclass
class BaseSettings(SettingsMixin):
    """Settings class relating to API requests."""

    api_key: Optional[str]
    """API Key for the client."""
    base_url: str
    request_timeout: int

    def __init__(self, api_key: Optional[str]):
        self._set_api_key(api_key)
        self.request_timeout = TIMEOUT_DEFAULT
        self.set_base_url(BASE_URL_DEFAULT)
        self.set_from_env()

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
