import httpx

from mindee.input.local_input_source import LocalInputSource
from mindee.input.url_input_source import URLInputSource
from mindee.parsing.common import StringDict
from mindee.v1.mindee_http.base_endpoint import BaseEndpoint
from mindee.v1.mindee_http.mindee_api import MindeeAPI


class Endpoint(BaseEndpoint):
    """Generic API endpoint for a product."""

    settings: MindeeAPI

    def __init__(
        self, url_name: str, owner: str, version: str, settings: MindeeAPI
    ) -> None:
        """
        Generic API endpoint for a product.

        :param owner: owner of the product
        :param url_name: name of the product as it appears in the URL
        :param version: interface version
        """
        super().__init__(settings)
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
        :param full_text: Whether to include the full OCR text response in compatible APIs.
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
        :param full_text: Whether to include the full OCR text response in compatible APIs.
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

        if workflow_id:
            url = f"{self.settings.base_url}/v1/workflows/{workflow_id}/{route}"
        else:
            url = f"{self.settings.url_root}/{route}"

        if isinstance(input_source, URLInputSource):
            data["document"] = input_source.url
            response = httpx.post(
                url=url,
                headers=self.settings.base_headers,
                data=data,
                params=params,
                timeout=self.settings.request_timeout,
            )
        else:
            files = {"document": input_source.read_contents(close_file)}
            response = httpx.post(
                url=url,
                files=files,
                headers=self.settings.base_headers,
                data=data,
                params=params,
                timeout=self.settings.request_timeout,
            )

        return response

    def document_queue_req_get(self, queue_id: str) -> httpx.Response:
        """
        Sends a request matching a given queue_id. Returns either a Job or a Document.

        :param queue_id: queue_id received from the API
        """
        return httpx.get(
            f"{self.settings.url_root}/documents/queue/{queue_id}",
            headers=self.settings.base_headers,
            timeout=self.settings.request_timeout,
            follow_redirects=True,
        )

    def openapi_get_req(self) -> httpx.Response:
        """Get the OpenAPI specification of the product."""
        return httpx.get(
            f"{self.settings.url_root}/openapi.json",
            headers=self.settings.base_headers,
            timeout=self.settings.request_timeout,
            follow_redirects=True,
        )

    def document_feedback_req_put(
        self, document_id: str, feedback: StringDict
    ) -> httpx.Response:
        """
        Send a feedback.

        :param document_id: ID of the document to send feedback to.
        :param feedback: Feedback object to send.
        """
        return httpx.put(
            f"{self.settings.base_url}/v1/documents/{document_id}/feedback",
            headers=self.settings.base_headers,
            data=feedback,
            timeout=self.settings.request_timeout,
        )


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
        files = {"document": input_source.read_contents(close_file)}
        params = {"training": True, "with_candidates": True}

        response = httpx.post(
            f"{self.settings.url_root}/predict",
            files=files,
            headers=self.settings.base_headers,
            params=params,
            timeout=self.settings.request_timeout,
        )
        return response

    def training_async_req_post(
        self, input_source: LocalInputSource, close_file: bool = True
    ) -> httpx.Response:
        """
        Make a request to POST a document for training without processing.

        :param input_source: Input object
        :return: httpx response
        :param close_file: Whether to `close()` the file after parsing it.
        """
        files = {"document": input_source.read_contents(close_file)}
        params = {"training": True, "async": True}

        response = httpx.post(
            f"{self.settings.url_root}/predict",
            files=files,
            headers=self.settings.base_headers,
            params=params,
            timeout=self.settings.request_timeout,
        )
        return response

    def document_req_del(self, document_id: str) -> httpx.Response:
        """
        Make a request to DELETE a document.

        :param document_id: ID of the document
        """
        response = httpx.delete(
            f"{self.settings.url_root}/documents/{document_id}",
            headers=self.settings.base_headers,
            timeout=self.settings.request_timeout,
        )
        return response

    def documents_req_get(self, page_id: int = 1) -> httpx.Response:
        """
        Make a request to GET info on all documents.

        :param page_id: Page number
        """
        params = {
            "page": page_id,
        }
        response = httpx.get(
            f"{self.settings.url_root}/documents",
            headers=self.settings.base_headers,
            params=params,
            timeout=self.settings.request_timeout,
            follow_redirects=True,
        )
        return response

    def document_req_get(self, document_id: str) -> httpx.Response:
        """
        Make a request to GET annotations for a document.

        :param document_id: ID of the document
        """
        params = {
            "include_annotations": True,
            "include_candidates": True,
            "global_orientation": True,
        }
        response = httpx.get(
            f"{self.settings.url_root}/documents/{document_id}",
            headers=self.settings.base_headers,
            params=params,
            timeout=self.settings.request_timeout,
            follow_redirects=True,
        )
        return response

    def annotations_req_post(
        self, document_id: str, annotations: dict
    ) -> httpx.Response:
        """
        Make a request to POST annotations for a document.

        :param document_id: ID of the document to annotate
        :param annotations: Annotations object
        :return: httpx response
        """
        response = httpx.post(
            f"{self.settings.url_root}/documents/{document_id}/annotations",
            headers=self.settings.base_headers,
            json=annotations,
            timeout=self.settings.request_timeout,
        )
        return response

    def annotations_req_put(
        self, document_id: str, annotations: dict
    ) -> httpx.Response:
        """
        Make a request to PUT annotations for a document.

        :param document_id: ID of the document to annotate
        :param annotations: Annotations object
        :return: httpx response
        """
        response = httpx.put(
            f"{self.settings.url_root}/documents/{document_id}/annotations",
            headers=self.settings.base_headers,
            json=annotations,
            timeout=self.settings.request_timeout,
        )
        return response

    def annotations_req_del(self, document_id: str) -> httpx.Response:
        """
        Make a request to DELETE annotations for a document.

        :param document_id: ID of the document to annotate
        :return: httpx response
        """
        response = httpx.delete(
            f"{self.settings.url_root}/documents/{document_id}/annotations",
            headers=self.settings.base_headers,
            timeout=self.settings.request_timeout,
        )
        return response
