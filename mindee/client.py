from pathlib import Path
from time import sleep
from typing import BinaryIO, Dict, Optional, Type, Union

from mindee.error.mindee_error import MindeeClientError, MindeeError
from mindee.error.mindee_http_error import handle_error
from mindee.input.page_options import PageOptions
from mindee.input.sources import (
    Base64Input,
    BytesInput,
    FileInput,
    LocalInputSource,
    PathInput,
    UrlInputSource,
)
from mindee.logger import logger
from mindee.mindee_http.endpoint import CustomEndpoint, Endpoint
from mindee.mindee_http.mindee_api import MindeeApi
from mindee.parsing.common.async_predict_response import AsyncPredictResponse
from mindee.parsing.common.feedback_response import FeedbackResponse
from mindee.parsing.common.inference import Inference, TypeInference
from mindee.parsing.common.predict_response import PredictResponse
from mindee.parsing.common.string_dict import StringDict

OTS_OWNER = "mindee"


def get_bound_classname(type_var) -> str:
    """Get the name of the bound class."""
    return type_var.__bound__.__name__


def _clean_account_name(account_name: str) -> str:
    """
    Checks that an account name is provided for custom builds, and sets the default one otherwise.

    :param product_class: product class to use for API calls.
    :param account_name: name of the account's holder. Only needed for custom products.
    """
    if not account_name or len(account_name) < 1:
        logger.warning(
            "No account name provided for custom build. %s will be used by default.",
            OTS_OWNER,
        )
        return OTS_OWNER
    return account_name


class Client:
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
    ) -> PredictResponse[TypeInference]:
        """
        Call prediction API on the document and parse the results.

        :param product_class: The document class to use.
            The response object will be instantiated based on this parameter.

        :param input_source: The document/source file to use.
            Has to be be created beforehand.

        :param include_words: Whether to include the full text for each page.
            This performs a full OCR operation on the server and will increase response time.

        :param close_file: Whether to ``close()`` the file after parsing it.
          Set to ``False`` if you need to access the file after this operation.

        :param page_options: If set, remove pages from the document as specified.
            This is done before sending the file to the server and is useful to avoid page limitations.

        :param cropper: Whether to include cropper results for each page.
            This performs a cropping operation on the server and will increase response time.

        :param endpoint: For custom endpoints, an endpoint has to be given.
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
        return self._make_request(
            product_class, input_source, endpoint, include_words, close_file, cropper
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
    ) -> AsyncPredictResponse:
        """
        Enqueueing to an async endpoint.

        :param product_class: The document class to use.
            The response object will be instantiated based on this parameter.

        :param input_source: The document/source file to use.
            Has to be be created beforehand.

        :param include_words: Whether to include the full text for each page.
            This performs a full OCR operation on the server and will increase response time.

        :param close_file: Whether to ``close()`` the file after parsing it.
          Set to ``False`` if you need to access the file after this operation.

        :param page_options: If set, remove pages from the document as specified.
            This is done before sending the file to the server and is useful to avoid page limitations.

        :param cropper: Whether to include cropper results for each page.
            This performs a cropping operation on the server and will increase response time.

        :param endpoint: For custom endpoints, an endpoint has to be given.
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
        return self._predict_async(
            product_class, input_source, include_words, close_file, cropper, endpoint
        )

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

    def _validate_async_params(
        self, initial_delay_sec: float, delay_sec: float
    ) -> None:
        if delay_sec < 2:
            raise MindeeClientError(
                "Cannot set auto-parsing delay to less than 2 seconds."
            )
        if initial_delay_sec < 4:
            raise MindeeClientError(
                "Cannot set initial parsing delay to less than 4 seconds."
            )

    def enqueue_and_parse(
        self,
        product_class: Type[Inference],
        input_source: Union[LocalInputSource, UrlInputSource],
        include_words: bool = False,
        close_file: bool = True,
        page_options: Optional[PageOptions] = None,
        cropper: bool = False,
        endpoint: Optional[Endpoint] = None,
        initial_delay_sec: float = 6,
        delay_sec: float = 3,
        max_retries: int = 10,
    ) -> AsyncPredictResponse:
        """
        Enqueueing to an async endpoint.

        :param product_class: The document class to use.
            The response object will be instantiated based on this parameter.

        :param input_source: The document/source file to use.
            Has to be be created beforehand.

        :param include_words: Whether to include the full text for each page.
            This performs a full OCR operation on the server and will increase response time.

        :param close_file: Whether to ``close()`` the file after parsing it.
          Set to ``False`` if you need to access the file after this operation.

        :param page_options: If set, remove pages from the document as specified.
            This is done before sending the file to the server and is useful to avoid page limitations.

        :param cropper: Whether to include cropper results for each page.
            This performs a cropping operation on the server and will increase response time.

        :param endpoint: For custom endpoints, an endpoint has to be given.

        :param initial_delay_sec: Delay between each polling attempts
            This should not be shorter than 4 seconds.

        :param delay_sec: Delay between each polling attempts
            This should not be shorter than 2 seconds.

        :param max_retries: Total amount of polling attempts.

        """
        self._validate_async_params(initial_delay_sec, delay_sec)
        if not endpoint:
            endpoint = self._initialize_ots_endpoint(product_class)
        queue_result = self.enqueue(
            product_class,
            input_source,
            include_words,
            close_file,
            page_options,
            cropper,
            endpoint,
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
        if not feedback_response.ok:
            raise handle_error(
                str(product_class.endpoint_name),
                feedback_response.json(),
                feedback_response.status_code,
            )

        return FeedbackResponse(feedback_response.json())

    def _make_request(
        self,
        product_class: Type[Inference],
        input_source: Union[LocalInputSource, UrlInputSource],
        endpoint: Endpoint,
        include_words: bool,
        close_file: bool,
        cropper: bool,
    ) -> PredictResponse:
        response = endpoint.predict_req_post(
            input_source, include_words, close_file, cropper
        )

        dict_response = response.json()

        if not response.ok:
            raise handle_error(
                str(product_class.endpoint_name),
                dict_response,
                response.status_code,
            )

        return PredictResponse(product_class, dict_response)

    def _predict_async(
        self,
        product_class: Type[Inference],
        input_source: Union[LocalInputSource, UrlInputSource],
        include_words: bool = False,
        close_file: bool = True,
        cropper: bool = False,
        endpoint: Optional[Endpoint] = None,
    ) -> AsyncPredictResponse:
        """
        Sends a document to the queue, and sends back an asynchronous predict response.

        :param doc_config: Configuration of the document.
        """
        if input_source is None:
            raise MindeeClientError("No input document provided")
        if not endpoint:
            endpoint = self._initialize_ots_endpoint(product_class)
        response = endpoint.predict_async_req_post(
            input_source, include_words, close_file, cropper
        )

        dict_response = response.json()

        if not response.ok:
            raise handle_error(
                str(product_class.endpoint_name),
                dict_response,
                response.status_code,
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
        :param doc_config: Pre-checked document configuration.
        """
        queue_response = endpoint.document_queue_req_get(queue_id=queue_id)

        if (
            not queue_response.status_code
            or queue_response.status_code < 200
            or queue_response.status_code > 302
        ):
            dict_response = queue_response.json()
            raise handle_error(
                str(product_class.endpoint_name),
                dict_response,
                queue_response.status_code,
            )

        return AsyncPredictResponse(product_class, queue_response.json())

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
        account_name: str,
        version: Optional[str] = None,
    ) -> Endpoint:
        """
        Add a custom endpoint, created using the Mindee API Builder.

        :param endpoint_name: The "API name" field in the "Settings" page of the API Builder
        :param account_name: Your organization's username on the API Builder
        :param version: If set, locks the version of the model to use.
            If not set, use the latest version of the model.
        :param product_class: A document class in which the response will be extracted.
            Must inherit from ``mindee.product.base.Document``.
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

    def source_from_path(
        self,
        input_path: Union[Path, str],
    ) -> PathInput:
        """
        Load a document from an absolute path, as a string.

        :param input_path: Path of file to open
        """
        return PathInput(input_path)

    def source_from_file(
        self,
        input_file: BinaryIO,
    ) -> FileInput:
        """
        Load a document from a normal Python file object/handle.

        :param input_file: Input file handle
        """
        return FileInput(
            input_file,
        )

    def source_from_b64string(
        self,
        input_string: str,
        filename: str,
    ) -> Base64Input:
        """
        Load a document from a base64 encoded string.

        :param input_string: Input to parse as base64 string
        :param filename: The name of the file (without the path)
        """
        return Base64Input(
            input_string,
            filename,
        )

    def source_from_bytes(
        self,
        input_bytes: bytes,
        filename: str,
    ) -> BytesInput:
        """
        Load a document from raw bytes.

        :param input_bytes: Raw byte input
        :param filename: The name of the file (without the path)
        """
        return BytesInput(
            input_bytes,
            filename,
        )

    def source_from_url(
        self,
        url: str,
    ) -> UrlInputSource:
        """
        Load a document from an URL.

        :param url: Raw byte input
        """
        return UrlInputSource(
            url,
        )
