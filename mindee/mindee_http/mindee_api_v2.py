import os
from typing import Dict, Optional

import requests

from mindee.error.mindee_error import MindeeApiV2Error
from mindee.input import LocalInputSource
from mindee.input.inference_predict_options import InferencePredictOptions
from mindee.logger import logger
from mindee.mindee_http.base_settings import USER_AGENT
from mindee.mindee_http.settings_mixin import SettingsMixin

API_KEY_V2_ENV_NAME = "MINDEE_V2_API_KEY"
API_KEY_V2_DEFAULT = ""

BASE_URL_ENV_NAME = "MINDEE_V2_BASE_URL"
BASE_URL_DEFAULT = "https://api-v2.mindee.net/v2"

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
            raise MindeeApiV2Error(
                (
                    f"Missing API key,"
                    " check your Client configuration.\n"
                    "You can set this using the "
                    f"'{API_KEY_V2_ENV_NAME}' environment variable."
                )
            )
        self.request_timeout = TIMEOUT_DEFAULT
        self.set_base_url(BASE_URL_DEFAULT)
        self.set_from_env()
        self.url_root = f"{self.base_url.rstrip('/')}"

    @property
    def base_headers(self) -> Dict[str, str]:
        """Base headers to send with all API requests."""
        return {
            "Authorization": self.api_key or "",
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

    def predict_async_req_post(
        self, input_source: LocalInputSource, options: InferencePredictOptions
    ) -> requests.Response:
        """
        Make an asynchronous request to POST a document for prediction on the V2 API.

        :param input_source: Input object.
        :param options: Options for the enqueueing of the document.
        :return: requests response.
        """
        data = {"model_id": options.model_id}
        url = f"{self.url_root}/inferences/enqueue"

        if options.full_text:
            data["full_text_ocr"] = "true"
        if options.rag:
            data["rag"] = "true"
        if options.webhook_ids and len(options.webhook_ids) > 0:
            data["webhook_ids"] = ",".join(options.webhook_ids)
        if options.alias and len(options.alias):
            data["alias"] = options.alias

        files = {"file": input_source.read_contents(options.close_file)}
        response = requests.post(
            url=url,
            files=files,
            headers=self.base_headers,
            data=data,
            timeout=self.request_timeout,
        )

        return response

    def get_inference_from_queue(self, queue_id: str) -> requests.Response:
        """
        Sends a request matching a given queue_id. Returns either a Job or a Document.

        :param queue_id: queue_id received from the API
        """
        return requests.get(
            f"{self.url_root}/jobs/{queue_id}",
            headers=self.base_headers,
            timeout=self.request_timeout,
        )
