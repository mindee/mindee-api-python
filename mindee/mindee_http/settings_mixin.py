from typing import Union


class SettingsMixin:
    """Settings mixin for V2 & V2 common methods & attributes."""

    base_url: str
    """Base URL for all V2 requests."""
    request_timeout: int
    """Timeout for all requests."""

    def set_timeout(self, value: Union[str, int]) -> None:
        """Set the timeout for all requests."""
        self.request_timeout = int(value)

    def set_base_url(self, value: str) -> None:
        """Set the base URL for all requests."""
        self.base_url = value
