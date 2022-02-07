import os
from typing import Optional

import requests

from mindee.versions import __version__, python_version, get_platform

MINDEE_API_URL = "https://api.mindee.net/v1"

API_TYPE_CUSTOM = "api_builder"
API_TYPE_OFF_THE_SHELF = "off_the_shelf"

PLATFORM = get_platform()


class Endpoint:
    owner: str
    url_name: str
    version: str
    key_name: str
    api_key: str = ""

    def __init__(
        self, owner: str, url_name: str, version: str, key_name: Optional[str] = None
    ):
        """
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

    @property
    def predict_url(self) -> str:
        """
        Return full HTTPS URL for a prediction request at a specific version
        :return: The full URL, i.e. https://api.mindee.net/v1/products/mindee/invoices/v2/predict
        """
        return f"{MINDEE_API_URL}/products/{self.owner}/{self.url_name}/v{self.version}/predict"

    @property
    def envvar_key_name(self) -> str:
        """
        The API key name as stored in the environment.
        """

        def to_envvar(name):
            return name.replace("-", "_").upper()

        key_name = to_envvar(self.key_name)
        if self.owner != "mindee":
            key_name = f"{to_envvar(self.owner)}_{key_name}"
        return f"MINDEE_{key_name}_API_KEY"

    def set_api_key_from_env(self):
        """
        Set the endpoint's API key from an environment variable, if present.
        """
        env_key = os.getenv(self.envvar_key_name, "")
        if env_key:
            self.api_key = env_key


def make_api_request(
    url: str, input_file, token: str, include_words: bool = False
) -> requests.Response:
    """
    :param input_file: Input object
    :param url: Endpoint url
    :param token: X-Inferuser-Token
    :param include_words: Include Mindee vision words in http_response
    :return: requests response
    """
    input_file.file_object.seek(0)
    files = {
        "document": (input_file.filename, input_file.file_object.read()),
    }
    input_file.file_object.close()

    headers = {
        "Authorization": f"Token {token}",
        "User-Agent": f"mindee-api-python@v{__version__} python-v{python_version} {PLATFORM}",
    }

    params = {}
    if include_words:
        params["include_mvision"] = "true"

    response = requests.post(url, files=files, headers=headers, data=params)
    return response


class HTTPException(Exception):
    def __init__(self, message):
        self.message = message
