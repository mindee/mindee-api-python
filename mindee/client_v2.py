from time import sleep
from typing import Optional, Union, Type, TypeVar

from mindee.client_mixin import ClientMixin
from mindee.error.mindee_error import MindeeError
from mindee.error.mindee_http_error_v2 import handle_error_v2
from mindee.input import UrlInputSource, SplitParameters
from mindee.input.inference_parameters import InferenceParameters
from mindee.input.polling_options import PollingOptions
from mindee.input.sources.local_input_source import LocalInputSource
from mindee.logger import logger
from mindee.mindee_http.mindee_api_v2 import MindeeApiV2
from mindee.mindee_http.response_validation_v2 import (
    is_valid_get_response,
    is_valid_post_response,
)
from mindee.parsing.v2.common_response import CommonStatus
from mindee.v2 import BaseInferenceResponse
from mindee.parsing.v2.inference_response import InferenceResponse
from mindee.parsing.v2.job_response import JobResponse

TypeBaseInferenceResponse = TypeVar(
    "TypeBaseInferenceResponse", bound=BaseInferenceResponse
)


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
        params: Union[InferenceParameters, SplitParameters],
        slug: Optional[str] = None,
    ) -> JobResponse:
        """
        Enqueues a document to a given model.

        :param input_source: The document/source file to use. Can be local or remote.
        :param params: Parameters to set when sending a file.
        :param slug: Slug for the endpoint.

        :return: A valid inference response.
        """
        logger.debug("Enqueuing inference using model: %s", params.model_id)
        response = self.mindee_api.req_post_inference_enqueue(
            input_source=input_source, params=params, slug=slug
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

    def get_inference(
        self,
        inference_id: str,
        inference_response_type: Type[BaseInferenceResponse] = InferenceResponse,
    ) -> BaseInferenceResponse:
        """
        Get the result of an inference that was previously enqueued.

        The inference will only be available after it has finished processing.

        :param inference_id: UUID of the inference to retrieve.
        :param inference_response_type: Class of the product to instantiate.
        :return: An inference response.
        """
        logger.debug("Fetching inference: %s", inference_id)
        slug = None
        if inference_response_type and inference_response_type is not InferenceResponse:
            slug = "utilities/" + inference_response_type.get_inference_slug()

        response = self.mindee_api.req_get_inference(inference_id, slug)
        if not is_valid_get_response(response):
            handle_error_v2(response.json())
        dict_response = response.json()
        return inference_response_type(dict_response)

    def _enqueue_and_get(
        self,
        input_source: Union[LocalInputSource, UrlInputSource],
        params: Union[InferenceParameters, SplitParameters],
        inference_response_type: Optional[
            Type[BaseInferenceResponse]
        ] = InferenceResponse,
    ) -> BaseInferenceResponse:
        """
        Enqueues to an asynchronous endpoint and automatically polls for a response.

        :param input_source: The document/source file to use. Can be local or remote.
        :param params: Parameters to set when sending a file.
        :param inference_response_type: The product class to use for the response object.

        :return: A valid inference response.
        """
        if not params.polling_options:
            params.polling_options = PollingOptions()
        self._validate_async_params(
            params.polling_options.initial_delay_sec,
            params.polling_options.delay_sec,
            params.polling_options.max_retries,
        )
        slug = None
        if inference_response_type and inference_response_type is not InferenceResponse:
            slug = "utilities/" + inference_response_type.get_inference_slug()
        enqueue_response = self.enqueue_inference(input_source, params, slug)
        logger.debug(
            "Successfully enqueued document with job id: %s", enqueue_response.job.id
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
                result = self.get_inference(
                    job_response.job.id, inference_response_type or InferenceResponse
                )
                return result
            try_counter += 1
            sleep(params.polling_options.delay_sec)

        raise MindeeError(f"Couldn't retrieve document after {try_counter + 1} tries.")

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
        response = self._enqueue_and_get(input_source, params)
        assert isinstance(response, InferenceResponse), (
            f'Invalid response type "{type(response)}"'
        )
        return response

    def enqueue_and_get_utility(
        self,
        inference_response_type: Type[TypeBaseInferenceResponse],
        input_source: Union[LocalInputSource, UrlInputSource],
        params: SplitParameters,
    ) -> TypeBaseInferenceResponse:
        """
        Enqueues to an asynchronous endpoint and automatically polls for a response.

        :param input_source: The document/source file to use. Can be local or remote.

        :param params: Parameters to set when sending a file.

        :param inference_response_type: The product class to use for the response object.

        :return: A valid inference response.
        """
        response = self._enqueue_and_get(input_source, params, inference_response_type)
        assert isinstance(response, inference_response_type), (
            f'Invalid response type "{type(response)}"'
        )
        return response
