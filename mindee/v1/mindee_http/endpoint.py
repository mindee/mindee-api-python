import httpx

from mindee.input.local_input_source import LocalInputSource
from mindee.input.url_input_source import URLInputSource
from mindee.parsing.common.string_dict import StringDict
from mindee.v1.mindee_http.base_endpoint import BaseEndpoint
from mindee.v1.mindee_http.mindee_api import MindeeAPI


class Endpoint(BaseEndpoint):
    """Generic API endpoint for a product."""

    settings: MindeeAPI

    def __init__(
        self,
        url_name: str,
        owner: str,
        version: str,
        settings: MindeeAPI,
        http_client: httpx.Client | None = None,
    ) -> None:
        """
        Generic API endpoint for a product.

        :param owner: owner of the product
        :param url_name: name of the product as it appears in the URL
        :param version: interface version
        :param settings: settings for the API
        :param http_client: HTTP client for making requests.
        """
        super().__init__(settings, http_client)
        self.owner = owner
        self.url_name = url_name
        self.version = version

    def predict_req_post(
        self,
        input_source: LocalInputSource | URLInputSource,
        include_words: bool = False,
        close_file: bool = True,
        cropper: bool = False,
        full_text: bool = False,
    ) -> httpx.Response:
        """
        Make a request to POST a document for prediction.

        :param input_source: Input object
        :param include_words: Include raw OCR words in the response
        :param close_file: Whether to `close()` the file after parsing it.
        :param cropper: Including Mindee cropping results.
        :param full_text: Whether to include the full OCR text response in compatible
        APIs.
        :return: httpx response
        """
        return self._custom_request(
            "predict", input_source, include_words, close_file, cropper, full_text
        )

    def predict_async_req_post(
        self,
        input_source: LocalInputSource | URLInputSource,
        include_words: bool = False,
        close_file: bool = True,
        cropper: bool = False,
        full_text: bool = False,
        workflow_id: str | None = None,
        rag: bool = False,
    ) -> httpx.Response:
        """
        Make an asynchronous request to POST a document for prediction.

        :param input_source: Input object
        :param include_words: Include raw OCR words in the response
        :param close_file: Whether to `close()` the file after parsing it.
        :param cropper: Including Mindee cropping results.
        :param full_text: Whether to include the full OCR text response in compatible
        APIs.
        :param workflow_id: Workflow ID.
        :param rag: If set, will enable Retrieval-Augmented Generation.
        :return: httpx response
        """
        return self._custom_request(
            "predict_async",
            input_source,
            include_words,
            close_file,
            cropper,
            full_text,
            workflow_id,
            rag,
        )

    def _custom_request(
        self,
        route: str,
        input_source: LocalInputSource | URLInputSource,
        include_words: bool = False,
        close_file: bool = True,
        cropper: bool = False,
        full_text: bool = False,
        workflow_id: str | None = None,
        rag: bool = False,
    ):
        data = {}
        if include_words:
            data["include_mvision"] = "true"

        params = {}
        if full_text:
            params["full_text_ocr"] = "true"
        if cropper:
            params["cropper"] = "true"
        if rag:
            params["rag"] = "true"

        post_kwargs: StringDict = {
            "headers": self.settings.base_headers,
            "data": data,
            "params": params,
            "timeout": self.settings.request_timeout,
        }

        if workflow_id:
            url = f"{self.settings.base_url}/v1/workflows/{workflow_id}/{route}"
        else:
            url = f"{self.settings.url_root}/{route}"

        if isinstance(input_source, URLInputSource):
            data["document"] = input_source.url
        else:
            post_kwargs["files"] = {"document": input_source.read_contents(close_file)}
        if self.http_client is None or self.http_client.is_closed:
            return httpx.post(url, **post_kwargs)
        return self.http_client.post(url, **post_kwargs)

    def document_queue_req_get(self, queue_id: str) -> httpx.Response:
        """
        Sends a request matching a given queue_id. Returns either a Job or a Document.

        :param queue_id: queue_id received from the API
        """
        url = f"{self.settings.url_root}/documents/queue/{queue_id}"
        get_kwargs: StringDict = {
            "headers": self.settings.base_headers,
            "timeout": self.settings.request_timeout,
            "follow_redirects": True,
        }
        if self.http_client is None or self.http_client.is_closed:
            return httpx.get(url, **get_kwargs)
        return self.http_client.get(url, **get_kwargs)

    def openapi_get_req(self) -> httpx.Response:
        """Get the OpenAPI specification of the product."""
        url = f"{self.settings.url_root}/openapi.json"
        get_kwargs: StringDict = {
            "headers": self.settings.base_headers,
            "timeout": self.settings.request_timeout,
            "follow_redirects": True,
        }
        if self.http_client is None or self.http_client.is_closed:
            return httpx.get(url, **get_kwargs)
        return self.http_client.get(url, **get_kwargs)

    def document_feedback_req_put(
        self, document_id: str, feedback: StringDict
    ) -> httpx.Response:
        """
        Send a feedback.

        :param document_id: ID of the document to send feedback to.
        :param feedback: Feedback object to send.
        """
        url = f"{self.settings.url_root}/documents/{document_id}/feedback"
        put_kwargs: StringDict = {
            "headers": self.settings.base_headers,
            "data": feedback,
            "timeout": self.settings.request_timeout,
        }
        if self.http_client is None or self.http_client.is_closed:
            return httpx.put(url, **put_kwargs)
        return self.http_client.put(url, **put_kwargs)


class CustomEndpoint(Endpoint):
    """Endpoint for all custom documents."""

    def training_req_post(
        self, input_source: LocalInputSource, close_file: bool = True
    ) -> httpx.Response:
        """
        Make a request to POST a document for training.

        :param input_source: Input object
        :return: httpx response
        :param close_file: Whether to `close()` the file after parsing it.
        """
        url = f"{self.settings.url_root}/predict"
        post_kwargs: StringDict = {
            "files": {"document": input_source.read_contents(close_file)},
            "headers": self.settings.base_headers,
            "params": {"training": True, "with_candidates": True},
            "timeout": self.settings.request_timeout,
        }
        if self.http_client is None or self.http_client.is_closed:
            return httpx.post(url, **post_kwargs)
        return self.http_client.post(url, **post_kwargs)

    def training_async_req_post(
        self, input_source: LocalInputSource, close_file: bool = True
    ) -> httpx.Response:
        """
        Make a request to POST a document for training without processing.

        :param input_source: Input object
        :return: httpx response
        :param close_file: Whether to `close()` the file after parsing it.
        """
        url = f"{self.settings.url_root}/predict"
        post_kwargs: StringDict = {
            "files": {"document": input_source.read_contents(close_file)},
            "headers": self.settings.base_headers,
            "params": {"training": True, "async": True},
            "timeout": self.settings.request_timeout,
        }
        if self.http_client is None or self.http_client.is_closed:
            return httpx.post(url, **post_kwargs)
        return self.http_client.post(url, **post_kwargs)

    def document_req_del(self, document_id: str) -> httpx.Response:
        """
        Make a request to DELETE a document.

        :param document_id: ID of the document
        """
        url = f"{self.settings.url_root}/documents/{document_id}"
        delete_kwargs: StringDict = {
            "headers": self.settings.base_headers,
            "timeout": self.settings.request_timeout,
        }
        if self.http_client is None or self.http_client.is_closed:
            return httpx.delete(url, **delete_kwargs)
        return httpx.delete(url, **delete_kwargs)

    def documents_req_get(self, page_id: int = 1) -> httpx.Response:
        """
        Make a request to GET info on all documents.

        :param page_id: Page number
        """
        url = f"{self.settings.url_root}/documents"
        get_kwargs: StringDict = {
            "headers": self.settings.base_headers,
            "params": {
                "page": page_id,
            },
            "timeout": self.settings.request_timeout,
            "follow_redirects": True,
        }
        if self.http_client is None or self.http_client.is_closed:
            return httpx.get(url, **get_kwargs)
        return self.http_client.get(url, **get_kwargs)

    def document_req_get(self, document_id: str) -> httpx.Response:
        """
        Make a request to GET annotations for a document.

        :param document_id: ID of the document
        """
        url = f"{self.settings.url_root}/documents/{document_id}"
        get_kwargs: StringDict = {
            "headers": self.settings.base_headers,
            "params": {
                "include_annotations": True,
                "include_candidates": True,
                "global_orientation": True,
            },
            "timeout": self.settings.request_timeout,
            "follow_redirects": True,
        }
        if self.http_client is None or self.http_client.is_closed:
            return httpx.get(url, **get_kwargs)
        return self.http_client.get(url, **get_kwargs)

    def annotations_req_post(
        self, document_id: str, annotations: dict
    ) -> httpx.Response:
        """
        Make a request to POST annotations for a document.

        :param document_id: ID of the document to annotate
        :param annotations: Annotations object
        :return: httpx response
        """
        url = f"{self.settings.url_root}/documents/{document_id}/annotations"
        post_kwargs: StringDict = {
            "headers": self.settings.base_headers,
            "json": annotations,
            "timeout": self.settings.request_timeout,
        }
        if self.http_client is None or self.http_client.is_closed:
            return httpx.post(url, **post_kwargs)
        return self.http_client.post(url, **post_kwargs)

    def annotations_req_put(
        self, document_id: str, annotations: dict
    ) -> httpx.Response:
        """
        Make a request to PUT annotations for a document.

        :param document_id: ID of the document to annotate
        :param annotations: Annotations object
        :return: httpx response
        """
        url = f"{self.settings.url_root}/documents/{document_id}/annotations"
        put_kwargs: StringDict = {
            "headers": self.settings.base_headers,
            "json": annotations,
            "timeout": self.settings.request_timeout,
        }
        if self.http_client is None or self.http_client.is_closed:
            return httpx.put(url, **put_kwargs)
        return self.http_client.put(url, **put_kwargs)

    def annotations_req_del(self, document_id: str) -> httpx.Response:
        """
        Make a request to DELETE annotations for a document.

        :param document_id: ID of the document to annotate
        :return: httpx response
        """
        url = f"{self.settings.url_root}/documents/{document_id}/annotations"
        delete_kwargs: StringDict = {
            "headers": self.settings.base_headers,
            "timeout": self.settings.request_timeout,
        }
        if self.http_client is None or self.http_client.is_closed:
            return httpx.delete(url, **delete_kwargs)
        return self.http_client.delete(url, **delete_kwargs)
