from typing import Dict, Optional

import requests

from mindee import InferencePredictOptions
from mindee.error.mindee_error import MindeeApiError
from mindee.input import LocalInputSource
from mindee.mindee_http.base_settings import USER_AGENT
from mindee.mindee_http.settings_mixin import SettingsMixin

API_KEY_V2_ENV_NAME = "MINDEE_V2_API_KEY"
API_KEY_V2_DEFAULT = ""

BASE_URL_ENV_NAME = "MINDEE_V2_BASE_URL"
BASE_URL_DEFAULT = "https://api-v2.mindee.com/v2"

REQUEST_TIMEOUT_ENV_NAME = "MINDEE_REQUEST_TIMEOUT"
TIMEOUT_DEFAULT = 120


class MindeeApiV2(SettingsMixin):
    """Settings class relating to API V2 requests."""

    url_root: str
    """Root of the URL to use for polling."""
    api_key: Optional[str]
    """API Key for the client."""

    def __init__(
        self,
        api_key: Optional[str],
    ):
        self.api_key = api_key
        if not self.api_key or len(self.api_key) == 0:
            raise MindeeApiError(
                (
                    f"Missing API key,"
                    " check your Client configuration.\n"
                    "You can set this using the "
                    f"'{API_KEY_V2_ENV_NAME}' environment variable."
                )
            )
        self.url_root = f"{self.base_url.rstrip('/')}"

    @property
    def base_headers(self) -> Dict[str, str]:
        """Base headers to send with all API requests."""
        return {
            "Authorization": f"Token {self.api_key}",
            "User-Agent": USER_AGENT,
        }

    def predict_async_req_post(
        self,
        input_source: LocalInputSource,
        options: InferencePredictOptions,
        close_file: bool = True,
    ) -> requests.Response:
        """
        Make an asynchronous request to POST a document for prediction on the V2 API.

        :param input_source: Input object.
        :param options: Options for the enqueueing of the document.
        :param close_file: Whether to `close()` the file after parsing it.
        :return: requests response.
        """
        data = {}
        params = {}
        url = f"{self.url_root}/inferences/enqueue"

        if options.full_text:
            params["full_text_ocr"] = "true"
        if options.rag:
            params["rag"] = "true"
        if options.webhook_ids and len(options.webhook_ids) > 0:
            params["webhook_ids"] = ",".join(options.webhook_ids)
        if options.alias and len(options.alias):
            data["alias"] = options.alias

        files = {"document": input_source.read_contents(close_file)}
        response = requests.post(
            url=url,
            files=files,
            headers=self.base_headers,
            data=data,
            params=params,
            timeout=self.request_timeout,
        )

        return response

    def document_queue_req_get(self, queue_id: str) -> requests.Response:
        """
        Sends a request matching a given queue_id. Returns either a Job or a Document.

        :param queue_id: queue_id received from the API
        """
        return requests.get(
            f"{self.url_root}/inferences/{queue_id}",
            headers=self.base_headers,
            timeout=self.request_timeout,
        )
