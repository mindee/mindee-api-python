from typing import Any, Dict, Generic, List, Optional, TypeVar

from mindee.document_config import DocumentConfig
from mindee.documents.base import Document
from mindee.input.sources import InputSource
from mindee.logger import logger

DocT = TypeVar("DocT", bound=Document)


class PredictResponse(Generic[DocT]):
    http_response: Dict[str, Any]
    """Raw HTTP response JSON"""
    document_type: str
    """Document type"""
    document: Optional[DocT]
    pages: List[DocT]

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
                    api_prediction=api_page["prediction"],
                    input_source=input_source,
                    page_n=api_page["id"],
                    document_type=doc_config.document_type,
                )
            )
        # https://github.com/python/mypy/issues/13596
        self.document = doc_config.document_class(  # type: ignore
            api_prediction=self.http_response["document"]["inference"]["prediction"],
            input_source=input_source,
            document_type=doc_config.document_type,
            page_n=None,
        )
