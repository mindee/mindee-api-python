import json
import os
from collections.abc import Callable
from typing import TypeVar

import httpx

from mindee.input.local_input_source import LocalInputSource
from mindee.input.url_input_source import URLInputSource
from mindee.logger import logger
from mindee.mindee_http.response_validation import is_valid_sync_response
from mindee.mindee_http.settings_mixin import SettingsMixin
from mindee.parsing.common.string_dict import StringDict
from mindee.v1.mindee_http.base_settings import USER_AGENT
from mindee.v2.client_options.base_product_parameters import BaseProductParameters
from mindee.v2.client_options.base_search_parameters import (
    BaseSearchParameters,
    TypeSearchResponse,
)
from mindee.v2.error.mindee_api_v2_error import MindeeAPIV2Error
from mindee.v2.error.mindee_http_error_v2 import (
    MindeeHTTPUnknownErrorV2,
    handle_error_v2,
)
from mindee.v2.parsing import BaseInferenceResponse
from mindee.v2.parsing.job.job_response import JobResponse
from mindee.v2.parsing.search.search_response import SearchResponse

API_KEY_V2_ENV_NAME = "MINDEE_V2_API_KEY"
API_KEY_V2_DEFAULT = ""

BASE_URL_ENV_NAME = "MINDEE_V2_BASE_URL"
BASE_URL_DEFAULT = "https://api-v2.mindee.net"

REQUEST_TIMEOUT_ENV_NAME = "MINDEE_REQUEST_TIMEOUT"
TIMEOUT_DEFAULT = 120

ResponseT = TypeVar("ResponseT", bound=BaseInferenceResponse)


class MindeeAPIV2(SettingsMixin):
    """Settings class relating to API V2 requests."""

    url_root: str
    """Root of the URL to use for polling."""
    api_key: str | None
    """API Key for the client."""
    http_client: httpx.Client | None
    """HTTP client for making requests."""
    request_timeout: float

    def __init__(self, api_key: str | None, http_client: httpx.Client | None = None):
        self.api_key = (
            api_key
            if api_key
            else os.environ.get(API_KEY_V2_ENV_NAME, API_KEY_V2_DEFAULT)
        )
        self.set_base_url(BASE_URL_DEFAULT)
        self._set_from_env()
        if not self.api_key:
            raise MindeeAPIV2Error(
                f"Missing API key,"
                " check your Client configuration.\n"
                "You can set this using the "
                f"'{API_KEY_V2_ENV_NAME}' environment variable."
            )
        self.url_root = f"{self.base_url.rstrip('/')}"
        self.http_client = http_client
        self.request_timeout = float(
            os.environ.get(REQUEST_TIMEOUT_ENV_NAME, TIMEOUT_DEFAULT)
        )

    @property
    def base_headers(self) -> dict[str, str]:
        """Base headers to send with all API requests."""
        return {
            "Authorization": self.api_key or "",
            "User-Agent": USER_AGENT,
        }

    def _set_from_env(self) -> None:
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

    def req_post_product_enqueue(
        self,
        input_source: LocalInputSource | URLInputSource,
        params: BaseProductParameters,
    ) -> JobResponse:
        """
        Send a file to the asynchronous processing queue for inference processing.

        :param input_source: Input object.
        :param params: Options for the enqueueing of the document.
        :return: httpx response.
        """
        data = params.get_request_parameters()
        slug = params.get_enqueue_slug()
        url = f"{self.url_root}/v2/products/{slug}/enqueue"
        post_kwargs: StringDict = {}
        if isinstance(input_source, LocalInputSource):
            post_kwargs["files"] = {
                "file": input_source.read_contents(params.close_file)
            }
        elif isinstance(input_source, URLInputSource):
            data["url"] = input_source.url

        post_caller: Callable
        if self.http_client is None or self.http_client.is_closed:
            post_caller = httpx.post
        else:
            post_caller = self.http_client.post

        response = post_caller(
            url,
            headers=self.base_headers,
            data=data,
            timeout=self.request_timeout,
            **post_kwargs,
        )
        dict_response = self._response_json(response)

        if not is_valid_sync_response(response):
            handle_error_v2(dict_response)
        return JobResponse(dict_response)

    def req_get_job_by_id(self, job_id: str) -> JobResponse:
        """
        Get the result of an inference that was previously enqueued.

        :param job_id: Job ID, returned by the enqueue request.
        """
        get_caller: Callable
        if self.http_client is None or self.http_client.is_closed:
            get_caller = httpx.get
        else:
            get_caller = self.http_client.get

        response = get_caller(
            url=f"{self.url_root}/v2/jobs/{job_id}",
            headers=self.base_headers,
            follow_redirects=False,
            timeout=self.request_timeout,
        )
        dict_response = self._response_json(response)
        if not is_valid_sync_response(response):
            handle_error_v2(dict_response)
        return JobResponse(dict_response)

    def req_get_product_result_by_url(
        self, response_type: type[ResponseT], url: str
    ) -> ResponseT:
        """
        Get the result of an inference that was previously enqueued.

        :param url: URL to use for the request.
        :param response_type: Type of the response to return.
        :return: Response object from the request.
        """
        get_caller: Callable
        if self.http_client is None or self.http_client.is_closed:
            get_caller = httpx.get
        else:
            get_caller = self.http_client.get

        response = get_caller(
            url=url,
            headers=self.base_headers,
            follow_redirects=False,
            timeout=self.request_timeout,
        )
        dict_response = self._response_json(response)
        if not is_valid_sync_response(response):
            handle_error_v2(dict_response)
        return response_type(dict_response)

    def req_get_product_result_by_id(
        self, response_type: type[ResponseT], inference_id: str
    ) -> ResponseT:
        """
        Sends a request matching a given queue_id. Returns either a Job or a Document.

        :param inference_id: Inference ID, returned by the job request.
        :param response_type: Type of the response to return.
        """
        slug = response_type.get_result_slug()
        return self.req_get_product_result_by_url(
            response_type=response_type,
            url=f"{self.url_root}/v2/products/{slug}/results/{inference_id}",
        )

    def req_search(
        self, params: BaseSearchParameters[TypeSearchResponse]
    ) -> TypeSearchResponse:
        """
        Search for resources matching the given criteria.
        :param params: Search parameters
        :return: A search response containing the matching resources
        """
        get_caller: Callable
        if self.http_client is None or self.http_client.is_closed:
            get_caller = httpx.get
        else:
            get_caller = self.http_client.get
        slug = params.get_slug()
        response_class = params.get_response_class()
        response = get_caller(
            url=f"{self.url_root}/v2/search/{slug}",
            headers=self.base_headers,
            params=params.get_request_parameters(),
            follow_redirects=False,
            timeout=self.request_timeout,
        )
        dict_response = self._response_json(response)
        if not is_valid_sync_response(response):
            handle_error_v2(dict_response)
        return response_class(dict_response)

    def req_get_search_models(
        self, name: str | None, model_type: str | None
    ) -> SearchResponse:
        """
        Searches for a list of models matching criteria.
        :param name: Name pattern to search for.
        :param model_type: Type of model to search for (exact match).
        :return: Response object containing search results.
        """
        get_caller: Callable
        if self.http_client is None or self.http_client.is_closed:
            get_caller = httpx.get
        else:
            get_caller = self.http_client.get
        params = {}
        if name:
            params["name"] = name
        if model_type:
            params["model_type"] = model_type

        response = get_caller(
            url=f"{self.url_root}/v2/search/models",
            headers=self.base_headers,
            params=params,
            follow_redirects=False,
            timeout=self.request_timeout,
        )
        dict_response = self._response_json(response)
        if not is_valid_sync_response(response):
            handle_error_v2(dict_response)
        return SearchResponse(dict_response)

    @staticmethod
    def _response_json(response: httpx.Response) -> StringDict:
        try:
            return response.json()
        except (httpx.DecodingError, json.JSONDecodeError) as e:
            raise MindeeHTTPUnknownErrorV2(
                f"HTTP {response.status_code} response is not valid JSON: "
                f"{response.text}"
            ) from e

    def close(self) -> None:
        """Closes the underlying HTTP client."""
        if self.http_client and not self.http_client.is_closed:
            self.http_client.close()

    def __enter__(self):
        self.http_client = httpx.Client()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def delete_http_client(self):
        """Delete the underlying HTTP client."""
        httpx_client = getattr(self, "http_client", None)
        if httpx_client and not self.http_client.is_closed:
            logger.info("Force-closing unclosed Mindee Client (V2) %s.", str(self))
            self.close()

    def __del__(self):
        """Ensure the HTTP client is closed when the object is garbage collected."""
        self.delete_http_client()
