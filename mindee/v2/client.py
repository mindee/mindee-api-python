from time import sleep
from typing import TypeVar

import httpx

from mindee.client_mixin import ClientMixin
from mindee.client_options.polling_options import PollingOptions
from mindee.error.mindee_error import MindeeError
from mindee.input import URLInputSource
from mindee.input.local_input_source import LocalInputSource
from mindee.logger import logger
from mindee.parsing.common.common_response import CommonStatus
from mindee.v2.client_options.base_parameters import BaseParameters
from mindee.v2.mindee_http.mindee_api_v2 import MindeeAPIV2
from mindee.v2.parsing.inference.base_response import BaseResponse
from mindee.v2.parsing.job.job_response import JobResponse
from mindee.v2.parsing.search.search_response import SearchResponse

TypeBaseResponse = TypeVar("TypeBaseResponse", bound=BaseResponse)


class Client(ClientMixin):
    """
    Mindee API Client.

    See: https://docs.mindee.com/
    """

    api_key: str | None
    mindee_api: MindeeAPIV2

    def __init__(
        self, api_key: str | None = None, http_client: httpx.Client | None = None
    ) -> None:
        """
        Mindee API Client.

        :param api_key: Your API key for all endpoints
        """
        self.api_key = api_key
        self.mindee_api = MindeeAPIV2(api_key, http_client)

    def enqueue(
        self,
        input_source: LocalInputSource | URLInputSource,
        params: BaseParameters,
    ) -> JobResponse:
        """
        Enqueues a document to a given model.

        :param input_source: The document/source file to use. Can be local or remote.
        :param params: Parameters to set when sending a file.

        :return: A valid inference response.
        """
        logger.debug("Enqueuing inference using model: %s", params.model_id)
        return self.mindee_api.enqueue(input_source, params)

    def get_job(self, job_id: str) -> JobResponse:
        """
        Get the status of an inference that was previously enqueued.

        Can be used for polling.

        :param job_id: UUID of the job to retrieve.
        :return: A job response.
        """
        logger.debug("Fetching job: %s", job_id)

        return self.mindee_api.get_job(job_id)

    def get_result(
        self,
        response_type: type[TypeBaseResponse],
        inference_id: str,
    ) -> TypeBaseResponse:
        """
        Get the result of an inference that was previously enqueued.

        The inference will only be available after it has finished processing.

        :param inference_id: UUID of the inference to retrieve.
        :param response_type: Class of the product to instantiate.
        :return: An inference response.
        """
        logger.debug("Fetching result: %s", inference_id)

        return self.mindee_api.get_result(response_type, inference_id)

    def get_result_from_url(
        self, response_type: type[TypeBaseResponse], url: str
    ) -> TypeBaseResponse:
        """
        Get the result of an inference that was previously enqueued by its URL.

        :param response_type: Type of the response to return.
        :param url: URL of the inference to retrieve.
        :return: The result of the inference.
        """
        return self.mindee_api.get_result_by_url(response_type, url)

    def enqueue_and_get_result(
        self,
        response_type: type[TypeBaseResponse],
        input_source: LocalInputSource | URLInputSource,
        params: BaseParameters,
    ) -> TypeBaseResponse:
        """
        Enqueues to an asynchronous endpoint and automatically polls for a response.

        :param input_source: The document/source file to use. Can be local or remote.
        :param params: Parameters to set when sending a file.
        :param response_type: The product class to use for the response object.

        :return: A valid inference response.
        """
        if not params.polling_options:
            params.polling_options = PollingOptions()
        self._validate_async_params(
            params.polling_options.initial_delay_sec,
            params.polling_options.delay_sec,
            params.polling_options.max_retries,
        )
        enqueue_response = self.enqueue(input_source, params)
        logger.debug(
            "Successfully enqueued document with job ID: %s", enqueue_response.job.id
        )
        sleep(params.polling_options.initial_delay_sec)
        try_counter = 0
        while try_counter < params.polling_options.max_retries:
            job_response = self.get_job(enqueue_response.job.id)
            assert isinstance(job_response, JobResponse)
            if job_response.job.status == CommonStatus.FAILED.value:
                if job_response.job.error:
                    detail = job_response.job.error.detail
                else:
                    detail = "No error detail available."
                raise MindeeError(
                    f"Parsing failed for job {job_response.job.id}: {detail}"
                )
            if (
                job_response.job.status == CommonStatus.PROCESSED.value
                and job_response.job.result_url
            ):
                logger.debug(
                    "Job ID %s completed processing at: %s",
                    job_response.job.id,
                    job_response.job.completed_at,
                )
                result = self.get_result_from_url(
                    response_type, job_response.job.result_url
                )
                assert isinstance(result, response_type), (
                    f'Invalid response type "{type(result)}"'
                )
                return result
            try_counter += 1
            sleep(params.polling_options.delay_sec)

        raise MindeeError(f"Couldn't retrieve document after {try_counter + 1} tries.")

    def search_models(
        self, name: str | None = None, model_type: str | None = None
    ) -> SearchResponse:
        """
        Get a list of models matching the provided name and type.

        :param name: Name of the model to filter by.
        :param model_type: Type of the model to filter by.
        :return: A list of models matching the provided criteria.
        """
        return self.mindee_api.get_models(name, model_type)

    def close(self) -> None:
        """Closes the underlying HTTP client."""
        self.mindee_api.http_client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
