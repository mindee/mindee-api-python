from time import sleep
from typing import Dict, Optional, Type, Union

from mindee.client_mixin import ClientMixin
from mindee.error.mindee_error import MindeeClientError, MindeeError
from mindee.error.mindee_http_error import handle_error
from mindee.input import WorkflowOptions
from mindee.input.local_response import LocalResponse
from mindee.input.page_options import PageOptions
from mindee.input.predict_options import AsyncPredictOptions, PredictOptions
from mindee.input.sources.local_input_source import LocalInputSource
from mindee.input.sources.url_input_source import UrlInputSource
from mindee.logger import logger
from mindee.mindee_http.endpoint import CustomEndpoint, Endpoint
from mindee.mindee_http.mindee_api import MindeeApi
from mindee.mindee_http.response_validation import (
    clean_request_json,
    is_valid_async_response,
    is_valid_sync_response,
)
from mindee.mindee_http.workflow_endpoint import WorkflowEndpoint
from mindee.mindee_http.workflow_settings import WorkflowSettings
from mindee.parsing.common.async_predict_response import AsyncPredictResponse
from mindee.parsing.common.feedback_response import FeedbackResponse
from mindee.parsing.common.inference import Inference
from mindee.parsing.common.predict_response import PredictResponse
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.workflow_response import WorkflowResponse
from mindee.product import GeneratedV1

OTS_OWNER = "mindee"


def get_bound_classname(type_var) -> str:
    """Get the name of the bound class."""
    return type_var.__bound__.__name__


def _clean_account_name(account_name: str) -> str:
    """
    Checks that an account name is provided for custom products, and sets the default one otherwise.

    :param account_name: name of the account's holder. Only needed for custom products.
    """
    if not account_name or len(account_name) < 1:
        logger.warning(
            "No account name provided for custom build. %s will be used by default.",
            OTS_OWNER,
        )
        return OTS_OWNER
    return account_name


class Client(ClientMixin):
    """
    Mindee API Client.

    See: https://developers.mindee.com/docs/
    """

    api_key: str

    def __init__(self, api_key: str = "") -> None:
        """
        Mindee API Client.

        :param api_key: Your API key for all endpoints
        """
        self.api_key = api_key

    def parse(
        self,
        product_class: Type[Inference],
        input_source: Union[LocalInputSource, UrlInputSource],
        include_words: bool = False,
        close_file: bool = True,
        page_options: Optional[PageOptions] = None,
        cropper: bool = False,
        endpoint: Optional[Endpoint] = None,
        full_text: bool = False,
    ) -> PredictResponse:
        """
        Call prediction API on the document and parse the results.

        :param product_class: The document class to use.
            The response object will be instantiated based on this parameter.

        :param input_source: The document/source file to use.
            Has to be created beforehand.

        :param include_words: Whether to include the full text for each page.
            This performs a full OCR operation on the server and will increase response time.
            Only available on financial document APIs.

        :param close_file: Whether to ``close()`` the file after parsing it.
          Set to ``False`` if you need to access the file after this operation.

        :param page_options: If set, remove pages from the document as specified.
            This is done before sending the file to the server.
            It is useful to avoid page limitations.

        :param cropper: Whether to include cropper results for each page.
            This performs a cropping operation on the server and will increase response time.

        :param endpoint: For custom endpoints, an endpoint has to be given.
        :param full_text: Whether to include the full OCR text response in compatible APIs.
        """
        if input_source is None:
            raise MindeeClientError("No input document provided.")

        if not endpoint:
            endpoint = self._initialize_ots_endpoint(product_class)

        logger.debug("Parsing document as '%s'", endpoint.url_name)

        if isinstance(input_source, LocalInputSource):
            if page_options and input_source.is_pdf():
                input_source.process_pdf(
                    page_options.operation,
                    page_options.on_min_pages,
                    page_options.page_indexes,
                )
        options = PredictOptions(cropper, full_text, include_words)
        return self._make_request(
            product_class,
            input_source,
            endpoint,
            options,
            close_file,
        )

    def enqueue(
        self,
        product_class: Type[Inference],
        input_source: Union[LocalInputSource, UrlInputSource],
        include_words: bool = False,
        close_file: bool = True,
        page_options: Optional[PageOptions] = None,
        cropper: bool = False,
        endpoint: Optional[Endpoint] = None,
        full_text: bool = False,
        workflow_id: Optional[str] = None,
        rag: bool = False,
    ) -> AsyncPredictResponse:
        """
        Enqueues a document to an asynchronous endpoint.

        :param product_class: The document class to use.
            The response object will be instantiated based on this parameter.

        :param input_source: The document/source file to use.
            Has to be created beforehand.

        :param include_words: Whether to include the full text for each page.
            This performs a full OCR operation on the server and will increase response time.

        :param close_file: Whether to ``close()`` the file after parsing it.
          Set to ``False`` if you need to access the file after this operation.

        :param page_options: If set, remove pages from the document as specified.
            This is done before sending the file to the server.
            It is useful to avoid page limitations.

        :param cropper: Whether to include cropper results for each page.
            This performs a cropping operation on the server and will increase response time.

        :param endpoint: For custom endpoints, an endpoint has to be given.

        :param full_text: Whether to include the full OCR text response in compatible APIs.

        :param workflow_id: Workflow ID.

        :param rag: If set, will enable Retrieval-Augmented Generation.
            Only works if a valid ``workflow_id`` is set.
        """
        if input_source is None:
            raise MindeeClientError("No input document provided.")

        if not endpoint:
            endpoint = self._initialize_ots_endpoint(product_class)

        logger.debug("Enqueuing document as '%s'", endpoint.url_name)

        if isinstance(input_source, LocalInputSource):
            if page_options and input_source.is_pdf():
                input_source.process_pdf(
                    page_options.operation,
                    page_options.on_min_pages,
                    page_options.page_indexes,
                )
        options = AsyncPredictOptions(
            cropper, full_text, include_words, workflow_id, rag
        )
        return self._predict_async(
            product_class,
            input_source,
            options,
            endpoint,
            close_file,
        )

    def load_prediction(
        self, product_class: Type[Inference], local_response: LocalResponse
    ) -> Union[AsyncPredictResponse, PredictResponse]:
        """
        Load a prediction.

        :param product_class: Class of the product to use.
        :param local_response: Local response to load.
        :return: A valid prediction.
        """
        try:
            if local_response.as_dict.get("job"):
                return AsyncPredictResponse(product_class, local_response.as_dict)
            return PredictResponse(product_class, local_response.as_dict)
        except KeyError as exc:
            raise MindeeError("No prediction found in local response.") from exc

    def parse_queued(
        self,
        product_class: Type[Inference],
        queue_id: str,
        endpoint: Optional[Endpoint] = None,
    ) -> AsyncPredictResponse:
        """
        Parses a queued document.

        :param product_class: The document class to use.
            The response object will be instantiated based on this parameter.
        :param queue_id: queue_id received from the API.
        :param endpoint: For custom endpoints, an endpoint has to be given.
        """
        if not endpoint:
            endpoint = self._initialize_ots_endpoint(product_class)

        logger.debug("Fetching queued document as '%s'", endpoint.url_name)

        return self._get_queued_document(product_class, endpoint, queue_id)

    def execute_workflow(
        self,
        input_source: Union[LocalInputSource, UrlInputSource],
        workflow_id: str,
        options: Optional[WorkflowOptions] = None,
        page_options: Optional[PageOptions] = None,
    ) -> WorkflowResponse:
        """
        Send the document to a workflow execution.

        :param input_source: The document/source file to use.
            Has to be created beforehand.
        :param workflow_id: ID of the workflow.
        :param page_options: If set, remove pages from the document as specified.
            This is done before sending the file to the server.
            It is useful to avoid page limitations.
        :param options: Options for the workflow.
        :return:
        """
        if isinstance(input_source, LocalInputSource):
            if page_options and input_source.is_pdf():
                input_source.process_pdf(
                    page_options.operation,
                    page_options.on_min_pages,
                    page_options.page_indexes,
                )

        if not options:
            options = WorkflowOptions(
                alias=None, priority=None, full_text=False, public_url=None, rag=False
            )
        logger.debug("Sending document to workflow: %s", workflow_id)
        return self._send_to_workflow(GeneratedV1, input_source, workflow_id, options)

    def enqueue_and_parse(  # pylint: disable=too-many-locals
        self,
        product_class: Type[Inference],
        input_source: Union[LocalInputSource, UrlInputSource],
        include_words: bool = False,
        close_file: bool = True,
        page_options: Optional[PageOptions] = None,
        cropper: bool = False,
        endpoint: Optional[Endpoint] = None,
        initial_delay_sec: float = 2,
        delay_sec: float = 1.5,
        max_retries: int = 80,
        full_text: bool = False,
        workflow_id: Optional[str] = None,
        rag: bool = False,
    ) -> AsyncPredictResponse:
        """
        Enqueues to an asynchronous endpoint and automatically polls for a response.

        :param product_class: The document class to use.
            The response object will be instantiated based on this parameter.

        :param input_source: The document/source file to use.
            Has to be created beforehand.

        :param include_words: Whether to include the full text for each page.
            This performs a full OCR operation on the server and will increase response time.

        :param close_file: Whether to ``close()`` the file after parsing it.
            Set to ``False`` if you need to access the file after this operation.

        :param page_options: If set, remove pages from the document as specified.
            This is done before sending the file to the server.
            It is useful to avoid page limitations.

        :param cropper: Whether to include cropper results for each page.
            This performs a cropping operation on the server and will increase response time.

        :param endpoint: For custom endpoints, an endpoint has to be given.

        :param initial_delay_sec: Delay between each polling attempts.
            This should not be shorter than 1 second.

        :param delay_sec: Delay between each polling attempts.
            This should not be shorter than 1 second.

        :param max_retries: Total amount of polling attempts.

        :param full_text: Whether to include the full OCR text response in compatible APIs.

        :param workflow_id: Workflow ID.

        :param rag: If set, will enable Retrieval-Augmented Generation.
            Only works if a valid ``workflow_id`` is set.
        """
        self._validate_async_params(initial_delay_sec, delay_sec, max_retries)
        if not endpoint:
            endpoint = self._initialize_ots_endpoint(product_class=product_class)
        queue_result = self.enqueue(
            product_class,
            input_source,
            include_words,
            close_file,
            page_options,
            cropper,
            endpoint,
            full_text,
            workflow_id,
            rag,
        )
        logger.debug(
            "Successfully enqueued document with job id: %s", queue_result.job.id
        )
        sleep(initial_delay_sec)
        retry_counter = 1
        poll_results = self.parse_queued(product_class, queue_result.job.id, endpoint)
        while retry_counter < max_retries:
            if poll_results.job.status == "completed":
                break
            if poll_results.job.status == "failed":
                raise MindeeError("Parsing failed for job {poll_results.job.id}")
            logger.debug(
                "Polling server for parsing result with job id: %s", queue_result.job.id
            )
            retry_counter += 1
            sleep(delay_sec)
            poll_results = self.parse_queued(
                product_class, queue_result.job.id, endpoint
            )

        if poll_results.job.status != "completed":
            raise MindeeError(
                f"Couldn't retrieve document after {retry_counter} tries."
            )

        return poll_results

    def send_feedback(
        self,
        product_class: Type[Inference],
        document_id: str,
        feedback: StringDict,
        endpoint: Optional[Endpoint] = None,
    ) -> FeedbackResponse:
        """
        Send a feedback for a document.

        :param product_class: The document class to use.
            The response object will be instantiated based on this parameter.

        :param document_id: The id of the document to send feedback to.
        :param feedback: Feedback to send.
        :param endpoint: For custom endpoints, an endpoint has to be given.
        """
        if not document_id or len(document_id) == 0:
            raise MindeeClientError("Invalid document_id.")
        if not endpoint:
            endpoint = self._initialize_ots_endpoint(product_class)

        feedback_response = endpoint.document_feedback_req_put(document_id, feedback)
        if not is_valid_sync_response(feedback_response):
            feedback_clean_response = clean_request_json(feedback_response)
            raise handle_error(
                str(product_class.endpoint_name),
                feedback_clean_response,
            )

        return FeedbackResponse(feedback_response.json())

    def _make_request(
        self,
        product_class: Type[Inference],
        input_source: Union[LocalInputSource, UrlInputSource],
        endpoint: Endpoint,
        options: PredictOptions,
        close_file: bool,
    ) -> PredictResponse:
        response = endpoint.predict_req_post(
            input_source,
            options.include_words,
            close_file,
            options.cropper,
            options.full_text,
        )
        dict_response = response.json()

        if not is_valid_sync_response(response):
            clean_response = clean_request_json(response)
            raise handle_error(
                str(product_class.endpoint_name),
                clean_response,
            )
        return PredictResponse(product_class, dict_response)

    def _predict_async(
        self,
        product_class: Type[Inference],
        input_source: Union[LocalInputSource, UrlInputSource],
        options: AsyncPredictOptions,
        endpoint: Optional[Endpoint] = None,
        close_file: bool = True,
    ) -> AsyncPredictResponse:
        """Sends a document to the queue, and sends back an asynchronous predict response."""
        if input_source is None:
            raise MindeeClientError("No input document provided")
        if not endpoint:
            endpoint = self._initialize_ots_endpoint(product_class)
        response = endpoint.predict_async_req_post(
            input_source=input_source,
            include_words=options.include_words,
            close_file=close_file,
            cropper=options.cropper,
            full_text=options.full_text,
            workflow_id=options.workflow_id,
            rag=options.rag,
        )
        dict_response = response.json()

        if not is_valid_async_response(response):
            clean_response = clean_request_json(response)
            raise handle_error(
                str(product_class.endpoint_name),
                clean_response,
            )

        return AsyncPredictResponse(product_class, dict_response)

    def _get_queued_document(
        self,
        product_class: Type[Inference],
        endpoint: Endpoint,
        queue_id: str,
    ) -> AsyncPredictResponse:
        """
        Fetches a document or a Job from a given queue.

        :param queue_id: Queue_id received from the API
        """
        queue_response = endpoint.document_queue_req_get(queue_id=queue_id)

        if not is_valid_async_response(queue_response):
            clean_queue_response = clean_request_json(queue_response)
            raise handle_error(
                str(product_class.endpoint_name),
                clean_queue_response,
            )

        return AsyncPredictResponse(product_class, queue_response.json())

    def _send_to_workflow(
        self,
        product_class: Type[Inference],
        input_source: Union[LocalInputSource, UrlInputSource],
        workflow_id: str,
        options: WorkflowOptions,
    ) -> WorkflowResponse:
        """
        Sends a document to a workflow.

        :param product_class: The document class to use.
            The response object will be instantiated based on this parameter.

        :param input_source: The document/source file to use.
            Has to be created beforehand.
        :param workflow_id: ID of the workflow.
        :param options: Optional options for the workflow.
        :return:
        """
        if input_source is None:
            raise MindeeClientError("No input document provided")

        workflow_endpoint = WorkflowEndpoint(
            WorkflowSettings(api_key=self.api_key, workflow_id=workflow_id)
        )

        response = workflow_endpoint.workflow_execution_post(input_source, options)

        dict_response = response.json()

        if not is_valid_async_response(response):
            clean_response = clean_request_json(response)
            raise handle_error(
                str(product_class.endpoint_name),
                clean_response,
            )
        return WorkflowResponse(product_class, dict_response)

    def _initialize_ots_endpoint(self, product_class: Type[Inference]) -> Endpoint:
        if product_class.__name__ == "CustomV1":
            raise MindeeClientError("Missing endpoint specifications for custom build.")
        endpoint_info: Dict[str, str] = product_class.get_endpoint_info(product_class)
        return self._build_endpoint(
            endpoint_info["name"], OTS_OWNER, endpoint_info["version"]
        )

    def _build_endpoint(
        self, endpoint_name: str, account_name: str, version: str
    ) -> Endpoint:
        api_settings = MindeeApi(
            api_key=self.api_key,
            endpoint_name=endpoint_name,
            account_name=account_name,
            version=version,
        )
        if account_name and len(account_name) > 0 and account_name != "mindee":
            return CustomEndpoint(endpoint_name, account_name, version, api_settings)
        return Endpoint(endpoint_name, account_name, version, api_settings)

    def create_endpoint(
        self,
        endpoint_name: str,
        account_name: str = "mindee",
        version: Optional[str] = None,
    ) -> Endpoint:
        """
        Add a custom endpoint, created using the Mindee API Builder.

        :param endpoint_name: The "API name" field in the "Settings" page of the API Builder
        :param account_name: Your organization's username on the API Builder
        :param version: If set, locks the version of the model to use.
            If not set, use the latest version of the model.
        """
        if len(endpoint_name) == 0:
            raise MindeeClientError("Custom endpoint require a valid 'endpoint_name'.")
        account_name = _clean_account_name(account_name)
        if not version or len(version) < 1:
            logger.debug(
                "No version provided for a custom build, will attempt to poll version 1 by default."
            )
            version = "1"
        return self._build_endpoint(endpoint_name, account_name, version)

    @staticmethod
    def source_from_url(
        url: str,
    ) -> UrlInputSource:
        """
        Load a document from a URL.

        :param url: Raw byte input
        """
        return UrlInputSource(
            url,
        )
