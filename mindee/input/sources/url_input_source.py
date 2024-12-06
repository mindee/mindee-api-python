from mindee.error.mindee_error import MindeeSourceError
from mindee.input import InputType
from mindee.logger import logger


class UrlInputSource:
    """A local or distant URL input."""

    url: str
    """The Uniform Resource Locator."""

    def __init__(self, url: str) -> None:
        """
        Input document from a base64 encoded string.

        :param url: URL to send, must be HTTPS
        """
        if not url.lower().startswith("https"):
            raise MindeeSourceError("URL must be HTTPS")

        self.input_type = InputType.URL

        logger.debug("URL input: %s", url)

        self.url = url
