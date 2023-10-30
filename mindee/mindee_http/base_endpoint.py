from abc import ABC

from mindee.mindee_http.mindee_api import MindeeApi


class BaseEndpoint(ABC):
    """Base endpoint class for the Mindee API."""

    def __init__(self, settings: MindeeApi) -> None:
        """
        Base API endpoint class for all endpoints.

        :param settings: Settings relating to all endpoints.
        """
        self.settings = settings
