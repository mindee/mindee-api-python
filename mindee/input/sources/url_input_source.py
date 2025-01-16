import os
import random
import string
from datetime import datetime
from pathlib import Path
from typing import Optional, Union
from urllib.parse import urlparse

import requests

from mindee.error.mindee_error import MindeeSourceError
from mindee.input.sources.bytes_input import BytesInput
from mindee.input.sources.input_type import InputType
from mindee.logger import logger


class UrlInputSource:
    """A local or distant URL input."""

    url: str
    """The Uniform Resource Locator."""

    def __init__(self, url: str) -> None:
        """
        Input document from a base64 encoded string.

        :param url: URL to send, must be HTTPS.
        """
        if not url.lower().startswith("https"):
            raise MindeeSourceError("URL must be HTTPS")

        self.input_type = InputType.URL

        logger.debug("URL input: %s", url)

        self.url = url

    def __fetch_file_content(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
        headers: Optional[dict] = None,
        max_redirects: int = 3,
    ) -> bytes:
        """
        Fetch the content of the file from the URL.

        :param username: Optional username for authentication.
        :param password: Optional password for authentication.
        :param token: Optional token for authentication.
        :param headers: Optional additional headers for the request.
        :param max_redirects: Maximum number of redirects to follow.
        :return: The content of the file as bytes.
        """
        if not headers:
            headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        auth = None if not username or not password else (username, password)

        response = UrlInputSource.__make_request(
            self.url, auth, headers, 0, max_redirects=max_redirects
        )

        return response

    def save_to_file(
        self,
        filepath: Union[Path, str],
        filename: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
        headers: Optional[dict] = None,
        max_redirects: int = 3,
    ) -> Path:
        """
        Save the content of the URL to a file.

        :param filepath: Path to save the content to.
        :param filename: Optional filename to give to the file.
        :param username: Optional username for authentication.
        :param password: Optional password for authentication.
        :param token: Optional token for authentication.
        :param headers: Optional additional headers for the request.
        :param max_redirects: Maximum number of redirects to follow.
        :return: The path to the saved file.
        """
        response = self.__fetch_file_content(
            username, password, token, headers, max_redirects
        )
        filename = self.__fill_filename(filename)
        full_path = Path(filepath) / filename
        with open(full_path, "wb") as binary_file:
            binary_file.write(response)
        return full_path

    def as_local_input_source(
        self,
        filename: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
        headers: Optional[dict] = None,
        max_redirects: int = 3,
    ) -> BytesInput:
        """
        Convert the URL content to a BytesInput object.

        :param filename: Optional filename for the BytesInput.
        :param username: Optional username for authentication.
        :param password: Optional password for authentication.
        :param token: Optional token for authentication.
        :param headers: Optional additional headers for the request.
        :param max_redirects: Maximum number of redirects to follow.
        :return: A BytesInput object containing the file content.
        """
        response = self.__fetch_file_content(
            username, password, token, headers, max_redirects
        )
        filename = self.__fill_filename(filename)

        return BytesInput(response, filename)

    @staticmethod
    def __extract_filename_from_url(uri) -> str:
        """
        Extract the filename from a given URL.

        :param uri: The URL to extract the filename from.
        :return: The extracted filename or an empty string if not found.
        """
        filename = os.path.basename(urlparse(uri).path)
        return filename if filename else ""

    @staticmethod
    def __generate_file_name(extension=".tmp") -> str:
        """
        Generate a unique filename with a timestamp and random string.

        :param extension: The file extension to use (default is '.tmp').
        :return: A generated filename.
        """
        random_string = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=8)
        )
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return f"mindee_temp_{timestamp}_{random_string}{extension}"

    @staticmethod
    def __get_file_extension(filename) -> Optional[str]:
        """
        Get the extension from a filename.

        :param filename: The filename to extract the extension from.
        :return: The lowercase file extension or None if not found.
        """
        ext = os.path.splitext(filename)[1]
        return ext.lower() if ext else None

    def __fill_filename(self, filename=None) -> str:
        """
        Fill in a filename if not provided or incomplete.

        :param filename: Optional filename to use.
        :return: A complete filename.
        """
        if filename is None:
            filename = UrlInputSource.__extract_filename_from_url(self.url)

        if not filename or not os.path.splitext(filename)[1]:
            filename = self.__generate_file_name(
                extension=UrlInputSource.__get_file_extension(filename)
            )

        return filename

    @staticmethod
    def __make_request(url, auth, headers, redirects, max_redirects) -> bytes:
        """
        Makes an HTTP request to the given URL, while following redirections.

        :param url: The URL to request.
        :param auth: Authentication tuple (username, password).
        :param headers: Headers for the request.
        :param redirects: Current number of redirects.
        :param max_redirects: Maximum number of redirects to follow.
        :return: The content of the response.
        :raises MindeeSourceError: If max redirects are exceeded or the request fails.
        """
        result = requests.get(url, headers=headers, timeout=120, auth=auth)
        if 299 < result.status_code < 400:
            if redirects == max_redirects:
                raise MindeeSourceError(
                    f"Can't reach URL after {redirects} out of {max_redirects} redirects, "
                    f"aborting operation."
                )
            return UrlInputSource.__make_request(
                redirects.location, auth, headers, redirects + 1, max_redirects
            )

        if result.status_code >= 400 or result.status_code < 200:
            raise MindeeSourceError(
                f"Couldn't retrieve file from server, error code {result.status_code}."
            )

        return result.content
