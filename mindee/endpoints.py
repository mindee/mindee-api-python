import os
from typing import Dict, Optional, Union

import requests

from mindee.input.sources import InputSource
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

OTS_OWNER = "mindee"


class Endpoint:
    """Generic API endpoint for a product."""

    owner: str
    url_name: str
    version: str
    api_key: str = API_KEY_DEFAULT
    _request_timeout: int = TIMEOUT_DEFAULT
    _base_url: str = BASE_URL_DEFAULT
    _url_root: str

    def __init__(
        self,
        owner: str,
        url_name: str,
        version: str,
        api_key: Optional[str] = None,
    ):
        """
        Generic API endpoint for a product.

        :param owner: owner of the product
        :param url_name: name of the product as it appears in the URL
        :param version: interface version
        """
        self.owner = owner
        self.url_name = url_name
        self.version = version
        if api_key:
            self.api_key = api_key
        else:
            self.set_api_key_from_env()
        self.set_from_env()

        self._url_root = (
            f"{self._base_url}/products/{self.owner}/{self.url_name}/v{self.version}"
        )

    @property
    def base_headers(self) -> Dict[str, str]:
        """Base headers to send with all API requests."""
        return {
            "Authorization": f"Token {self.api_key}",
            "User-Agent": USER_AGENT,
        }

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
        self._request_timeout = int(value)

    def set_base_url(self, value: str) -> None:
        """Set the base URL for all requests."""
        self._base_url = value

    def set_api_key_from_env(self) -> None:
        """Set the endpoint's API key from an environment variable, if present."""
        env_val = os.getenv(API_KEY_ENV_NAME, "")
        if env_val:
            self.api_key = env_val
            logger.debug("API key set from environment")

    def predict_req_post(
        self,
        input_source: InputSource,
        include_words: bool = False,
        close_file: bool = True,
        cropper: bool = False,
    ) -> requests.Response:
        """
        Make a request to POST a document for prediction.

        :param input_source: Input object
        :param include_words: Include raw OCR words in the response
        :param close_file: Whether to `close()` the file after parsing it.
        :param cropper: Including Mindee cropping results.
        :return: requests response
        """
        files = {"document": input_source.read_contents(close_file)}
        data = {}
        if include_words:
            data["include_mvision"] = "true"

        params = {}
        if cropper:
            params["cropper"] = "true"

        response = requests.post(
            f"{self._url_root}/predict",
            files=files,
            headers=self.base_headers,
            data=data,
            params=params,
            timeout=self._request_timeout,
        )
        return response


class CustomEndpoint(Endpoint):
    def training_req_post(
        self, input_source: InputSource, close_file: bool = True
    ) -> requests.Response:
        """
        Make a request to POST a document for training.

        :param input_source: Input object
        :return: requests response
        :param close_file: Whether to `close()` the file after parsing it.
        """
        files = {"document": input_source.read_contents(close_file)}
        params = {"training": True, "with_candidates": True}

        response = requests.post(
            f"{self._url_root}/predict",
            files=files,
            headers=self.base_headers,
            params=params,
            timeout=self._request_timeout,
        )
        return response

    def training_async_req_post(
        self, input_source: InputSource, close_file: bool = True
    ) -> requests.Response:
        """
        Make a request to POST a document for training without processing.

        :param input_source: Input object
        :return: requests response
        :param close_file: Whether to `close()` the file after parsing it.
        """
        files = {"document": input_source.read_contents(close_file)}
        params = {"training": True, "async": True}

        response = requests.post(
            f"{self._url_root}/predict",
            files=files,
            headers=self.base_headers,
            params=params,
            timeout=self._request_timeout,
        )
        return response

    def document_req_get(self, document_id: str) -> requests.Response:
        """
        Make a request to GET annotations for a document.

        :param document_id: ID of the document
        """
        params = {
            "include_annotations": True,
            "include_candidates": True,
            "global_orientation": True,
        }
        response = requests.get(
            f"{self._url_root}/documents/{document_id}",
            headers=self.base_headers,
            params=params,
            timeout=self._request_timeout,
        )
        return response

    def document_req_del(self, document_id: str) -> requests.Response:
        """
        Make a request to DELETE a document.

        :param document_id: ID of the document
        """
        response = requests.delete(
            f"{self._url_root}/documents/{document_id}",
            headers=self.base_headers,
            timeout=self._request_timeout,
        )
        return response

    def documents_req_get(self, page_n: int = 1) -> requests.Response:
        """
        Make a request to GET info on all documents.

        :param page_n: Page number
        """
        params = {
            "page": page_n,
        }
        response = requests.get(
            f"{self._url_root}/documents",
            headers=self.base_headers,
            params=params,
            timeout=self._request_timeout,
        )
        return response

    def annotations_req_post(
        self, document_id: str, annotations: dict
    ) -> requests.Response:
        """
        Make a request to POST annotations for a document.

        :param document_id: ID of the document to annotate
        :param annotations: Annotations object
        :return: requests response
        """
        response = requests.post(
            f"{self._url_root}/documents/{document_id}/annotations",
            headers=self.base_headers,
            json=annotations,
            timeout=self._request_timeout,
        )
        return response

    def annotations_req_put(
        self, document_id: str, annotations: dict
    ) -> requests.Response:
        """
        Make a request to PUT annotations for a document.

        :param document_id: ID of the document to annotate
        :param annotations: Annotations object
        :return: requests response
        """
        response = requests.put(
            f"{self._url_root}/documents/{document_id}/annotations",
            headers=self.base_headers,
            json=annotations,
            timeout=self._request_timeout,
        )
        return response

    def annotations_req_del(self, document_id: str) -> requests.Response:
        """
        Make a request to DELETE annotations for a document.

        :param document_id: ID of the document to annotate
        :return: requests response
        """
        response = requests.delete(
            f"{self._url_root}/documents/{document_id}/annotations",
            headers=self.base_headers,
            timeout=self._request_timeout,
        )
        return response


class StandardEndpoint(Endpoint):
    def __init__(self, url_name: str, version: str, api_key: Optional[str] = None):
        super().__init__(
            owner=OTS_OWNER,
            url_name=url_name,
            version=version,
            api_key=api_key,
        )


class HTTPException(RuntimeError):
    """An exception relating to HTTP calls."""
