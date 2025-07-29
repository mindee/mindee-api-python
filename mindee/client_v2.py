from time import sleep
from typing import Optional, Union

from mindee.client_mixin import ClientMixin
from mindee.error.mindee_error import MindeeError
from mindee.error.mindee_http_error_v2 import handle_error_v2
from mindee.input import UrlInputSource
from mindee.input.inference_parameters import InferenceParameters
from mindee.input.polling_options import PollingOptions
from mindee.input.sources.local_input_source import LocalInputSource
from mindee.logger import logger
from mindee.mindee_http.mindee_api_v2 import MindeeApiV2
from mindee.mindee_http.response_validation_v2 import (
    is_valid_get_response,
    is_valid_post_response,
)
from mindee.parsing.v2.field.common_response import CommonStatus
from mindee.parsing.v2.inference_response import InferenceResponse
from mindee.parsing.v2.job_response import JobResponse


class ClientV2(ClientMixin):
    """
    Mindee API Client.

    See: https://developers.mindee.com/docs/
    """

    api_key: Optional[str]
    mindee_api: MindeeApiV2

    def __init__(self, api_key: Optional[str] = None) -> None:
        """
        Mindee API Client.

        :param api_key: Your API key for all endpoints
        """
        self.api_key = api_key
        self.mindee_api = MindeeApiV2(api_key)

    def enqueue_inference(
        self,
        input_source: Union[LocalInputSource, UrlInputSource],
        params: InferenceParameters,
    ) -> JobResponse:
        """
        Enqueues a document to a given model.

        :param input_source: The document/source file to use. Can be local or remote.

        :param params: Parameters to set when sending a file.
        :return: A valid inference response.
        """
        logger.debug("Enqueuing inference using model: %s", params.model_id)

        response = self.mindee_api.req_post_inference_enqueue(
            input_source=input_source, params=params
        )
        dict_response = response.json()

        if not is_valid_post_response(response):
            handle_error_v2(dict_response)
        return JobResponse(dict_response)

    def get_job(self, job_id: str) -> JobResponse:
        """
        Get the status of an inference that was previously enqueued.

        Can be used for polling.

        :param job_id: UUID of the job to retrieve.
        :return: A job response.
        """
        logger.debug("Fetching job: %s", job_id)

        response = self.mindee_api.req_get_job(job_id)
        if not is_valid_get_response(response):
            handle_error_v2(response.json())
        dict_response = response.json()
        return JobResponse(dict_response)

    def get_inference(self, inference_id: str) -> InferenceResponse:
        """
        Get the result of an inference that was previously enqueued.

        The inference will only be available after it has finished processing.

        :param inference_id: UUID of the inference to retrieve.
        :return: An inference response.
        """
        logger.debug("Fetching inference: %s", inference_id)

        response = self.mindee_api.req_get_inference(inference_id)
        if not is_valid_get_response(response):
            handle_error_v2(response.json())
        dict_response = response.json()
        return InferenceResponse(dict_response)

    def enqueue_and_get_inference(
        self,
        input_source: Union[LocalInputSource, UrlInputSource],
        params: InferenceParameters,
    ) -> InferenceResponse:
        """
        Enqueues to an asynchronous endpoint and automatically polls for a response.

        :param input_source: The document/source file to use. Can be local or remote.

        :param params: Parameters to set when sending a file.

        :return: A valid inference response.
        """
        if not params.polling_options:
            params.polling_options = PollingOptions()
        self._validate_async_params(
            params.polling_options.initial_delay_sec,
            params.polling_options.delay_sec,
            params.polling_options.max_retries,
        )
        enqueue_response = self.enqueue_inference(input_source, params)
        logger.debug(
            "Successfully enqueued inference with job id: %s", enqueue_response.job.id
        )
        sleep(params.polling_options.initial_delay_sec)
        try_counter = 0
        while try_counter < params.polling_options.max_retries:
            job_response = self.get_job(enqueue_response.job.id)
            if job_response.job.status == CommonStatus.FAILED.value:
                if job_response.job.error:
                    detail = job_response.job.error.detail
                else:
                    detail = "No error detail available."
                raise MindeeError(
                    f"Parsing failed for job {job_response.job.id}: {detail}"
                )
            if job_response.job.status == CommonStatus.PROCESSED.value:
                return self.get_inference(job_response.job.id)
            try_counter += 1
            sleep(params.polling_options.delay_sec)

        raise MindeeError(f"Couldn't retrieve document after {try_counter + 1} tries.")
