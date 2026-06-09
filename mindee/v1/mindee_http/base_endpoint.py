import httpx

from mindee.v1.mindee_http.base_settings import BaseSettings


class BaseEndpoint:
    """Base endpoint class for the Mindee API."""

    settings: BaseSettings
    """Settings relating to all endpoints."""
    http_client: httpx.Client | None
    """HTTP client for making requests."""

    def __init__(
        self, settings: BaseSettings, http_client: httpx.Client | None = None
    ) -> None:
        """
        Base API endpoint class for all endpoints.

        :param settings: Settings relating to all endpoints.
        :param http_client: HTTP client for making requests.
        """
        self.settings = settings
        self.http_client = http_client
