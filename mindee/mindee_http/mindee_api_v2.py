import os
from typing import Dict, Optional, Union

import requests

from mindee.error.mindee_error import MindeeApiV2Error
from mindee.input import LocalInputSource, UrlInputSource
from mindee.input.inference_parameters import InferenceParameters
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

    def req_post_inference_enqueue(
        self,
        input_source: Union[LocalInputSource, UrlInputSource],
        params: InferenceParameters,
    ) -> requests.Response:
        """
        Make an asynchronous request to POST a document for prediction on the V2 API.

        :param input_source: Input object.
        :param params: Options for the enqueueing of the document.
        :return: requests response.
        """
        data = {"model_id": params.model_id}
        url = f"{self.url_root}/inferences/enqueue"

        if params.rag:
            data["rag"] = "true"
        if params.webhook_ids and len(params.webhook_ids) > 0:
            data["webhook_ids"] = ",".join(params.webhook_ids)
        if params.alias and len(params.alias):
            data["alias"] = params.alias

        if isinstance(input_source, LocalInputSource):
            files = {"file": input_source.read_contents(params.close_file)}
            response = requests.post(
                url=url,
                files=files,
                headers=self.base_headers,
                data=data,
                timeout=self.request_timeout,
            )
        elif isinstance(input_source, UrlInputSource):
            data["url"] = input_source.url
            response = requests.post(
                url=url,
                headers=self.base_headers,
                data=data,
                timeout=self.request_timeout,
            )
        else:
            raise MindeeApiV2Error("Invalid input source.")
        return response

    def req_get_job(self, job_id: str) -> requests.Response:
        """
        Sends a request matching a given queue_id. Returns either a Job or a Document.

        :param job_id: Job ID, returned by the enqueue request.
        """
        return requests.get(
            f"{self.url_root}/jobs/{job_id}",
            headers=self.base_headers,
            timeout=self.request_timeout,
            allow_redirects=False,
        )

    def req_get_inference(self, inference_id: str) -> requests.Response:
        """
        Sends a request matching a given queue_id. Returns either a Job or a Document.

        :param inference_id: Inference ID, returned by the job request.
        """
        return requests.get(
            f"{self.url_root}/inferences/{inference_id}",
            headers=self.base_headers,
            timeout=self.request_timeout,
            allow_redirects=False,
        )
