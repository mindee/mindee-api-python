from abc import ABC

from mindee.mindee_http.base_settings import BaseSettings


class BaseEndpoint(ABC):
    """Base endpoint class for the Mindee API."""

    def __init__(self, settings: BaseSettings) -> None:
        """
        Base API endpoint class for all endpoints.

        :param settings: Settings relating to all endpoints.
        """
        self.settings = settings
