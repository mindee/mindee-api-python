import os
from typing import Optional

import requests

from mindee.inputs import InputDocument
from mindee.logger import logger
from mindee.versions import __version__, get_platform, python_version

MINDEE_API_URL = "https://api.mindee.net/v1"
PLATFORM = get_platform()
USER_AGENT = f"mindee-api-python@v{__version__} python-v{python_version} {PLATFORM}"

INVOICE_VERSION = "3"
INVOICE_URL_NAME = "invoices"

RECEIPT_VERSION = "3"
RECEIPT_URL_NAME = "expense_receipts"

PASSPORT_VERSION = "1"
PASSPORT_URL_NAME = "passport"


class Endpoint:
    """Generic API endpoint for a product."""

    owner: str
    url_name: str
    version: str
    key_name: str
    api_key: str = ""
    _url_root: str

    def __init__(
        self,
        owner: str,
        url_name: str,
        version: str,
        key_name: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        """
        Generic API endpoint for a product.

        :param owner: owner of the product
        :param url_name: name of the product as it appears in the URL
        :param version: interface version
        :param key_name: where to find the key in envvars
        """
        self.owner = owner
        self.url_name = url_name
        self.version = version
        if key_name:
            self.key_name = key_name
        else:
            self.key_name = url_name
        if api_key:
            self.api_key = api_key
        else:
            self.set_api_key_from_env()

        self._url_root = (
            f"{MINDEE_API_URL}/products/{self.owner}/{self.url_name}/v{self.version}"
        )

    @property
    def base_headers(self):
        """Base headers to send with all API requests."""
        return {
            "Authorization": f"Token {self.api_key}",
            "User-Agent": USER_AGENT,
        }

    @property
    def envvar_key_name(self) -> str:
        """The API key name as stored in the environment."""

        def to_envvar(name) -> str:
            return name.replace("-", "_").upper()

        key_name = to_envvar(self.key_name)
        if self.owner != "mindee":
            key_name = f"{to_envvar(self.owner)}_{key_name}"
        return f"MINDEE_{key_name}_API_KEY"

    def set_api_key_from_env(self) -> None:
        """Set the endpoint's API key from an environment variable, if present."""
        env_key = os.getenv(self.envvar_key_name, "")
        if env_key:
            self.api_key = env_key
            logger.debug("Set from environment: %s", self.envvar_key_name)

    def predict_request(
        self,
        input_file: InputDocument,
        include_words: bool = False,
        close_file: bool = True,
    ) -> requests.Response:
        """
        Make a prediction request.

        :param input_file: Input object
        :param include_words: Include raw OCR words in the response
        :param close_file: Whether to `close()` the file after parsing it.
        :return: requests response
        """
        files = {"document": input_file.read_contents(close_file)}
        data = {}
        if include_words:
            data["include_mvision"] = "true"

        response = requests.post(
            f"{self._url_root}/predict",
            files=files,
            headers=self.base_headers,
            data=data,
        )
        return response


class CustomEndpoint(Endpoint):
    def training_request(
        self, input_file: InputDocument, close_file: bool = True
    ) -> requests.Response:
        """
        Make a training request.

        :param input_file: Input object
        :return: requests response
        :param close_file: Whether to `close()` the file after parsing it.
        """
        files = {"document": input_file.read_contents(close_file)}
        params = {"training": True, "with_candidates": True}

        response = requests.post(
            f"{self._url_root}/predict",
            files=files,
            headers=self.base_headers,
            params=params,
        )
        return response

    def annotation_request(
        self, document_id: str, annotations: dict
    ) -> requests.Response:
        """
        Make an annotation request.

        :param document_id: ID of the document to annotate
        :param annotations: Annotations object
        :return: requests response
        """
        response = requests.post(
            f"{self._url_root}/documents/{document_id}/annotations",
            headers=self.base_headers,
            json=annotations,
        )
        return response


class InvoiceEndpoint(Endpoint):
    def __init__(self, api_key: Optional[str] = None):
        owner = "mindee"
        url_name = INVOICE_URL_NAME
        version = INVOICE_VERSION
        key_name = "invoice"
        super().__init__(
            owner=owner,
            url_name=url_name,
            version=version,
            key_name=key_name,
            api_key=api_key,
        )


class ReceiptEndpoint(Endpoint):
    def __init__(self, api_key: Optional[str] = None):
        owner = "mindee"
        url_name = RECEIPT_URL_NAME
        version = RECEIPT_VERSION
        key_name = "receipt"
        super().__init__(
            owner=owner,
            url_name=url_name,
            version=version,
            key_name=key_name,
            api_key=api_key,
        )


class PassportEndpoint(Endpoint):
    def __init__(self, api_key: Optional[str] = None):
        owner = "mindee"
        url_name = PASSPORT_URL_NAME
        version = PASSPORT_VERSION
        super().__init__(
            owner=owner,
            url_name=url_name,
            version=version,
            api_key=api_key,
        )


class HTTPException(RuntimeError):
    """An exception relating to HTTP calls."""
