import warnings
from time import sleep

import httpx

from mindee.client_options.polling_options import PollingOptions
from mindee.error.mindee_error import MindeeError
from mindee.input import URLInputSource
from mindee.input.local_input_source import LocalInputSource
from mindee.logger import logger
from mindee.mindee_http.cancellation_token import CancellationToken
from mindee.parsing.common.common_response import CommonStatus
from mindee.v2.client_options.base_annotation_parameters import BaseAnnotationParameters
from mindee.v2.client_options.base_product_parameters import BaseProductParameters
from mindee.v2.client_options.base_rag_document_upload_parameters import (
    BaseRagDocumentUploadParameters,
)
from mindee.v2.client_options.base_search_parameters import (
    BaseSearchParameters,
    TypeSearchResponse,
)
from mindee.v2.mindee_http.mindee_api_v2 import MindeeAPIV2
from mindee.v2.parsing.base_rag_annotation_response import (
    TypeRagAnnotationResponse,
)
from mindee.v2.parsing.inference.base_inference_response import (
    TypeBaseInferenceResponse,
)
from mindee.v2.parsing.job.job_response import JobResponse
from mindee.v2.parsing.search.search_response import SearchResponse


class Client:
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
        params: BaseProductParameters,
    ) -> JobResponse:
        """
        Enqueues a document to a given model.

        :param input_source: The document/source file to use. Can be local or remote.
        :param params: Parameters to set when sending a file.

        :return: A valid inference response.
        """
        logger.debug("Enqueuing inference using model: %s", params.model_id)
        return self.mindee_api.req_post_product_enqueue(input_source, params)

    def get_job(self, job_id: str) -> JobResponse:
        """
        Get the status of an inference that was previously enqueued.

        Can be used for polling.

        :param job_id: UUID of the job to retrieve.
        :return: A job response.
        """
        logger.debug("Fetching job: %s", job_id)

        return self.mindee_api.req_get_job_by_id(job_id)

    def get_result(
        self,
        response_type: type[TypeBaseInferenceResponse],
        inference_id: str,
    ) -> TypeBaseInferenceResponse:
        """
        Get the result of an inference that was previously enqueued by its ID.

        The inference will only be available after it has finished processing.

        :param inference_id: UUID of the inference to retrieve.
        :param response_type: Class of the product to instantiate.
        :return: An inference response.
        """
        logger.debug("Fetching result: %s", inference_id)

        return self.mindee_api.req_get_product_result_by_id(response_type, inference_id)

    def get_result_from_url(
        self, response_type: type[TypeBaseInferenceResponse], url: str
    ) -> TypeBaseInferenceResponse:
        """
        Get the result of an inference that was previously enqueued by its URL.

        :param response_type: Type of the response to return.
        :param url: URL of the inference to retrieve.
        :return: The result of the inference.
        """
        return self.mindee_api.req_get_product_result_by_url(response_type, url)

    def enqueue_and_get_result(
        self,
        response_type: type[TypeBaseInferenceResponse],
        input_source: LocalInputSource | URLInputSource,
        params: BaseProductParameters,
        cancellation_token: CancellationToken | None = None,
    ) -> TypeBaseInferenceResponse:
        """
        Enqueues to an asynchronous endpoint and automatically polls for a response.

        :param input_source: The document/source file to use. Can be local or remote.
        :param params: Parameters to set when sending a file.
        :param response_type: The product class to use for the response object.
        :param cancellation_token: A cancellation token that can be used to cancel the
        request.

        :return: A valid inference response.
        """
        if not params.polling_options:
            params.polling_options = PollingOptions()
        params.polling_options.validate_settings()
        enqueue_response = self.enqueue(input_source, params)
        logger.debug(
            "Successfully enqueued document with job ID: %s", enqueue_response.job.id
        )
        if cancellation_token and cancellation_token.is_canceled:
            raise MindeeError("Request canceled through cancellation token.")
        sleep(params.polling_options.initial_delay_sec)
        try_counter = 0
        while try_counter < params.polling_options.max_retries:
            if cancellation_token and cancellation_token.is_canceled:
                raise MindeeError("Request canceled through cancellation token.")
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

    def upload_rag_document(
        self,
        input_source: LocalInputSource,
        parameters: BaseRagDocumentUploadParameters[TypeRagAnnotationResponse],
    ) -> TypeRagAnnotationResponse:
        """
        Not recommended for general use, prefer ``upload_and_get_rag_document``.
        You will need to poll until the document is ready for use.
        Add a document to the RAG database.
        """
        return self.mindee_api.req_post_rag_document(input_source, parameters)

    def upload_and_get_rag_document(
        self,
        input_source: LocalInputSource,
        parameters: BaseRagDocumentUploadParameters[TypeRagAnnotationResponse],
        polling_options: PollingOptions | None = None,
        cancellation_token: CancellationToken | None = None,
    ) -> TypeRagAnnotationResponse:
        """
        Add a document to the RAG database and return the initial annotation.
        """
        initial_response = self.upload_rag_document(input_source, parameters)
        if initial_response.status != "Processing":
            return initial_response
        if polling_options is None:
            polling_options = PollingOptions()
        return self._poll_for_rag_document(
            initial_response, polling_options, cancellation_token
        )

    def get_rag_document(
        self, response_type: type[TypeRagAnnotationResponse], document_id: str
    ) -> TypeRagAnnotationResponse:
        """
        Not recommended for general use, prefer ``get_ready_rag_document``.
        You will need to poll until the document is ready for use.
        Get a document's info and annotations from the RAG database.
        """
        return self.mindee_api.req_get_rag_annotation(response_type, document_id)

    def get_ready_rag_document(
        self,
        response_type: type[TypeRagAnnotationResponse],
        document_id: str,
        polling_options: PollingOptions | None = None,
        cancellation_token: CancellationToken | None = None,
    ):
        """
        Get a document's info and annotations from the RAG database.
        """
        initial_response = self.get_rag_document(response_type, document_id)
        if initial_response.status != "Processing":
            return initial_response
        if polling_options is None:
            polling_options = PollingOptions()
        return self._poll_for_rag_document(
            initial_response, polling_options, cancellation_token
        )

    def update_rag_annotations(
        self, parameters: BaseAnnotationParameters[TypeRagAnnotationResponse]
    ) -> TypeRagAnnotationResponse:
        """
        Not recommended for general use, prefer ``update_and_get_rag_annotations``.
        You will need to poll until the document is ready for use.
        Update a document's annotations in the RAG database.
        """
        return self.mindee_api.req_patch_rag_annotation(parameters)

    def update_and_get_rag_annotations(
        self,
        parameters: BaseAnnotationParameters[TypeRagAnnotationResponse],
        polling_options: PollingOptions | None = None,
        cancellation_token: CancellationToken | None = None,
    ) -> TypeRagAnnotationResponse:
        """
        Update a document's annotations in the RAG database.
        """
        initial_response = self.update_rag_annotations(parameters)
        if initial_response.status != "Processing":
            return initial_response
        if polling_options is None:
            polling_options = PollingOptions()
        return self._poll_for_rag_document(
            initial_response, polling_options, cancellation_token
        )

    def delete_extraction_rag_document(self, document_id: str) -> bool:
        """
        Delete a document from the RAG database.
        For extraction models only.
        """
        return self.mindee_api.req_delete_extraction_rag_document(document_id)

    def _poll_for_rag_document(
        self,
        initial_response: TypeRagAnnotationResponse,
        polling_options: PollingOptions,
        cancellation_token: CancellationToken | None = None,
    ) -> TypeRagAnnotationResponse:
        """
        Poll until the document is finished processing or the max number of attempts is reached.
        """
        logger.info("Polling for RAG document ID: %s", initial_response.id)
        polling_options.validate_settings()
        max_retries = polling_options.max_retries + 1

        logger.debug(
            "Waiting %s seconds before attempting to retrieve the result...",
            polling_options.initial_delay_sec,
        )

        if cancellation_token and cancellation_token.is_canceled:
            raise MindeeError("Request canceled through cancellation token.")

        sleep(polling_options.initial_delay_sec)
        document_id = initial_response.id
        retry_count = 1

        while retry_count < max_retries:
            if cancellation_token and cancellation_token.is_canceled:
                raise MindeeError("Request canceled through cancellation token.")
            logger.info("Poll attempt %s of %s", retry_count, max_retries)

            response = self.get_rag_document(type(initial_response), document_id)
            retry_count += 1

            if response.status == "Processing":
                sleep(polling_options.delay_sec)
                continue
            if response.status == "Failed":
                raise MindeeError("Job failed without an error payload.")
            return response

        raise MindeeError(f"RAG polling not complete after {retry_count - 1} attempts.")

    def search(
        self, params: BaseSearchParameters[TypeSearchResponse]
    ) -> TypeSearchResponse:
        """
        Search for resources matching the given criteria.
        :param params: Search parameters
        :return: A search response containing the matching resources
        """
        return self.mindee_api.req_search(params)

    def search_models(
        self, name: str | None = None, model_type: str | None = None
    ) -> SearchResponse:
        """
        Deprecated: use `search` instead.
        """
        warnings.warn(
            "search_models is deprecated, use search instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.mindee_api.req_get_search_models(name, model_type)

    def close(self) -> None:
        """Closes the underlying HTTP client."""
        self.mindee_api.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        """Ensure the HTTP client is closed when the object is garbage collected."""
        mindee_api = getattr(self, "mindee_api", None)
        if mindee_api:
            httpx_client = getattr(self.mindee_api, "http_client", None)
            if httpx_client and self.mindee_api:
                self.mindee_api.delete_http_client()
