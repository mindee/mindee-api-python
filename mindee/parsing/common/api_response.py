from typing import Any, Dict, Generic, List, Optional, Union

from mindee.input.sources import LocalInputSource, UrlInputSource
from mindee.logger import logger
from mindee.parsing.common.api_request import ApiRequest
from mindee.parsing.common.document import TypeApiPrediction, TypeDocument
from mindee.parsing.common.job import Job
from mindee.parsing.common.ocr import Ocr
from mindee.product.config import DocumentConfig


class PredictResponse(Generic[TypeDocument]):
    """
    Response of a prediction request.

    This is a generic class, so certain class properties depend on the document type.
    """

    http_response: TypeApiPrediction
    """Raw HTTP response JSON"""
    document_type: Optional[str] = None
    """Document type"""
    input_path: Optional[str] = None
    """Path of the input file"""
    input_filename: Optional[str] = None
    """Name of the input file"""
    input_mimetype: Optional[str] = None
    """MIME type of the input file"""
    document: Optional[TypeDocument]
    """An instance of the ``Document`` class, according to the type given."""
    pages: List[TypeDocument]
    """A list of instances of the ``Document`` class, according to the type given."""
    ocr: Optional[Ocr]
    """Full OCR operation results."""

    def __init__(
        self,
        doc_config: DocumentConfig,
        http_response: Dict[str, Any],
        input_source: Optional[Union[LocalInputSource, UrlInputSource]],
        response_ok: bool,
    ) -> None:
        """
        Container for the raw API response and the parsed document.

        :param doc_config: DocumentConfig
        :param input_source: Input object
        :param http_response: json response from HTTP call
        """
        logger.debug("Handling API response")
        self.http_response = http_response
        self.document_type = doc_config.document_type
        self.pages = []

        if isinstance(input_source, LocalInputSource):
            self.input_path = input_source.filepath
            self.input_filename = input_source.filename
            self.input_mimetype = input_source.file_mimetype

        if not response_ok:
            self.document = None
            self.ocr = None
        else:
            self._load_response(doc_config, input_source)
            self.ocr = self._load_ocr(http_response)

    @staticmethod
    def _load_ocr(http_response: TypeApiPrediction):
        ocr_prediction = http_response["document"].get("ocr", None)
        if not ocr_prediction or not ocr_prediction.get("mvision-v1", None):
            return None
        return Ocr(ocr_prediction)

    def _load_response(
        self,
        doc_config: DocumentConfig,
        input_source: Optional[Union[LocalInputSource, UrlInputSource]],
    ) -> None:
        # This is some seriously ugly stuff.
        # Simplify all this in V4, as we won't need to pass the document type anymore
        for api_page in self.http_response["document"]["inference"]["pages"]:
            if doc_config.document_type:
                # https://github.com/python/mypy/issues/13596
                page = doc_config.document_class(
                    api_prediction=api_page,
                    input_source=input_source,
                    document_type=doc_config.document_type,
                    page_n=api_page["id"],
                )
            else:
                page = doc_config.document_class(  # type: ignore
                    api_prediction=api_page,
                    input_source=input_source,
                    page_n=api_page["id"],
                )
            self.pages.append(page)  # type: ignore

        # https://github.com/python/mypy/issues/13596
        if doc_config.document_type:
            self.document = doc_config.document_class(  # type: ignore
                api_prediction=self.http_response["document"]["inference"],
                input_source=input_source,
                document_type=doc_config.document_type,
                page_n=None,
            )
        else:
            self.document = doc_config.document_class(  # type: ignore
                api_prediction=self.http_response["document"]["inference"],
                input_source=input_source,
                page_n=None,
            )


class AsyncPredictResponse(Generic[TypeDocument]):
    """
    Async Response Wrapper class for a Predict response.

    Links a Job to a future PredictResponse.
    """

    api_request: ApiRequest
    job: Job
    """Job object link to the prediction. As long as it isn't complete, the prediction doesn't exist."""
    document: Optional[PredictResponse[TypeDocument]]

    def __init__(
        self,
        http_response: Dict[str, Any],
        doc_config: DocumentConfig,
        input_source: Optional[Union[LocalInputSource, UrlInputSource]],
        response_ok: bool,
    ) -> None:
        """
        Container wrapper for a raw API response.

        Inherits and instantiates a normal PredictResponse if the parsing of
        the current queue is both requested and done.

        :param doc_config: DocumentConfig
        :param input_source: Input object
        :param http_response: json response from HTTP call
        """
        self.document = PredictResponse[TypeDocument](
            http_response=http_response,
            doc_config=doc_config,
            input_source=input_source,
            response_ok=response_ok and http_response["job"]["status"] == "completed",
        )
        self.job = Job(http_response["job"])
        self.api_request = ApiRequest(http_response["api_request"])