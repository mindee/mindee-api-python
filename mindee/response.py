from typing import Any, Dict, Generic, List, Optional

from mindee.documents.base import TypeDocument
from mindee.documents.config import DocumentConfig
from mindee.input.sources import InputSource
from mindee.logger import logger


class PredictResponse(Generic[TypeDocument]):
    """
    Response of a prediction request.

    This is a generic class, so certain class properties depend on the document type.
    """

    http_response: Dict[str, Any]
    """Raw HTTP response JSON"""
    document_type: str
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

    def __init__(
        self,
        doc_config: DocumentConfig,
        http_response: dict,
        input_source: InputSource,
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

        if input_source:
            self.input_path = input_source.filepath
            self.input_filename = input_source.filename
            self.input_mimetype = input_source.file_mimetype

        if not response_ok:
            self.document = None
        else:
            self._load_response(doc_config, input_source)

    def _load_response(
        self,
        doc_config: DocumentConfig,
        input_source: InputSource,
    ) -> None:
        for api_page in self.http_response["document"]["inference"]["pages"]:
            self.pages.append(
                # https://github.com/python/mypy/issues/13596
                doc_config.document_class(  # type: ignore
                    api_prediction=api_page,
                    input_source=input_source,
                    document_type=doc_config.document_type,
                    page_n=api_page["id"],
                )
            )
        # https://github.com/python/mypy/issues/13596
        self.document = doc_config.document_class(  # type: ignore
            api_prediction=self.http_response["document"]["inference"],
            input_source=input_source,
            document_type=doc_config.document_type,
            page_n=None,
        )
