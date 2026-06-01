import json
from typing import Optional, Union

import requests
from requests import Response

from mindee.input.local_input_source import LocalInputSource
from mindee.input.url_input_source import URLInputSource
from mindee.v1.mindee_http.base_endpoint import BaseEndpoint
from mindee.v1.mindee_http.mindee_api import MindeeAPI
from mindee.parsing.common import StringDict


class Endpoint(BaseEndpoint):
    """Generic API endpoint for a product."""

    settings: MindeeAPI

    def __init__(
        self, url_name: str, owner: str, version: str, settings: MindeeAPI
    ) -> None:
        """
        Generic API endpoint for a product.

        :params owner: owner of the product
        :params url_name: name of the product as it appears in the URL
        :params version: interface version
        """
        super().__init__(settings)
        self.owner = owner
        self.url_name = url_name
        self.version = version

    def predict_req_post(
        self,
        input_source: Union[LocalInputSource, URLInputSource],
        include_words: bool = False,
        close_file: bool = True,
        cropper: bool = False,
        full_text: bool = False,
    ) -> requests.Response:
        """
        Make a request to POST a document for prediction.

        :params input_source: Input object
        :params include_words: Include raw OCR words in the response
        :params close_file: Whether to `close()` the file after parsing it.
        :params cropper: Including Mindee cropping results.
        :params full_text: Whether to include the full OCR text response in compatible APIs.
        :return: requests response
        """
        return self._custom_request(
            "predict", input_source, include_words, close_file, cropper, full_text
        )

    def predict_async_req_post(
        self,
        input_source: Union[LocalInputSource, URLInputSource],
        include_words: bool = False,
        close_file: bool = True,
        cropper: bool = False,
        full_text: bool = False,
        workflow_id: Optional[str] = None,
        rag: bool = False,
    ) -> requests.Response:
        """
        Make an asynchronous request to POST a document for prediction.

        :params input_source: Input object
        :params include_words: Include raw OCR words in the response
        :params close_file: Whether to `close()` the file after parsing it.
        :params cropper: Including Mindee cropping results.
        :params full_text: Whether to include the full OCR text response in compatible APIs.
        :params workflow_id: Workflow ID.
        :params rag: If set, will enable Retrieval-Augmented Generation.
        :return: requests response
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
        input_source: Union[LocalInputSource, URLInputSource],
        include_words: bool = False,
        close_file: bool = True,
        cropper: bool = False,
        full_text: bool = False,
        workflow_id: Optional[str] = None,
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
            url = f"{self.settings.base_url}/workflows/{workflow_id}/{route}"
        else:
            url = f"{self.settings.url_root}/{route}"

        if isinstance(input_source, URLInputSource):
            data["document"] = input_source.url
            response = requests.post(
                url=url,
                headers=self.settings.base_headers,
                data=data,
                params=params,
                timeout=self.settings.request_timeout,
            )
        else:
            files = {"document": input_source.read_contents(close_file)}
            response = requests.post(
                url=url,
                files=files,
                headers=self.settings.base_headers,
                data=data,
                params=params,
                timeout=self.settings.request_timeout,
            )

        return response

    def document_queue_req_get(self, queue_id: str) -> requests.Response:
        """
        Sends a request matching a given queue_id. Returns either a Job or a Document.

        :params queue_id: queue_id received from the API
        """
        return requests.get(
            f"{self.settings.url_root}/documents/queue/{queue_id}",
            headers=self.settings.base_headers,
            timeout=self.settings.request_timeout,
        )

    def openapi_get_req(self) -> Response:
        """Get the OpenAPI specification of the product."""
        return requests.get(
            f"{self.settings.url_root}/openapi.json",
            headers=self.settings.base_headers,
            timeout=self.settings.request_timeout,
        )

    def document_feedback_req_put(
        self, document_id: str, feedback: StringDict
    ) -> Response:
        """
        Send a feedback.

        :params document_id: ID of the document to send feedback to.
        :params feedback: Feedback object to send.
        """
        return requests.put(
            f"{self.settings.base_url}/documents/{document_id}/feedback",
            headers=self.settings.base_headers,
            data=json.dumps(feedback, indent=0),
            timeout=self.settings.request_timeout,
        )


class CustomEndpoint(Endpoint):
    """Endpoint for all custom documents."""

    def training_req_post(
        self, input_source: LocalInputSource, close_file: bool = True
    ) -> requests.Response:
        """
        Make a request to POST a document for training.

        :params input_source: Input object
        :return: requests response
        :params close_file: Whether to `close()` the file after parsing it.
        """
        files = {"document": input_source.read_contents(close_file)}
        params = {"training": True, "with_candidates": True}

        response = requests.post(
            f"{self.settings.url_root}/predict",
            files=files,
            headers=self.settings.base_headers,
            params=params,
            timeout=self.settings.request_timeout,
        )
        return response

    def training_async_req_post(
        self, input_source: LocalInputSource, close_file: bool = True
    ) -> requests.Response:
        """
        Make a request to POST a document for training without processing.

        :params input_source: Input object
        :return: requests response
        :params close_file: Whether to `close()` the file after parsing it.
        """
        files = {"document": input_source.read_contents(close_file)}
        params = {"training": True, "async": True}

        response = requests.post(
            f"{self.settings.url_root}/predict",
            files=files,
            headers=self.settings.base_headers,
            params=params,
            timeout=self.settings.request_timeout,
        )
        return response

    def document_req_del(self, document_id: str) -> requests.Response:
        """
        Make a request to DELETE a document.

        :params document_id: ID of the document
        """
        response = requests.delete(
            f"{self.settings.url_root}/documents/{document_id}",
            headers=self.settings.base_headers,
            timeout=self.settings.request_timeout,
        )
        return response

    def documents_req_get(self, page_id: int = 1) -> requests.Response:
        """
        Make a request to GET info on all documents.

        :params page_id: Page number
        """
        params = {
            "page": page_id,
        }
        response = requests.get(
            f"{self.settings.url_root}/documents",
            headers=self.settings.base_headers,
            params=params,
            timeout=self.settings.request_timeout,
        )
        return response

    def document_req_get(self, document_id: str) -> requests.Response:
        """
        Make a request to GET annotations for a document.

        :params document_id: ID of the document
        """
        params = {
            "include_annotations": True,
            "include_candidates": True,
            "global_orientation": True,
        }
        response = requests.get(
            f"{self.settings.url_root}/documents/{document_id}",
            headers=self.settings.base_headers,
            params=params,
            timeout=self.settings.request_timeout,
        )
        return response

    def annotations_req_post(
        self, document_id: str, annotations: dict
    ) -> requests.Response:
        """
        Make a request to POST annotations for a document.

        :params document_id: ID of the document to annotate
        :params annotations: Annotations object
        :return: requests response
        """
        response = requests.post(
            f"{self.settings.url_root}/documents/{document_id}/annotations",
            headers=self.settings.base_headers,
            json=annotations,
            timeout=self.settings.request_timeout,
        )
        return response

    def annotations_req_put(
        self, document_id: str, annotations: dict
    ) -> requests.Response:
        """
        Make a request to PUT annotations for a document.

        :params document_id: ID of the document to annotate
        :params annotations: Annotations object
        :return: requests response
        """
        response = requests.put(
            f"{self.settings.url_root}/documents/{document_id}/annotations",
            headers=self.settings.base_headers,
            json=annotations,
            timeout=self.settings.request_timeout,
        )
        return response

    def annotations_req_del(self, document_id: str) -> requests.Response:
        """
        Make a request to DELETE annotations for a document.

        :params document_id: ID of the document to annotate
        :return: requests response
        """
        response = requests.delete(
            f"{self.settings.url_root}/documents/{document_id}/annotations",
            headers=self.settings.base_headers,
            timeout=self.settings.request_timeout,
        )
        return response
