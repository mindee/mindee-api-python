from typing import Any, Dict, List

from mindee.document_config import DocumentConfig
from mindee.documents.base import Document, TypeDocument
from mindee.logger import logger


class DocumentResponse:
    http_response: Dict[str, Any]
    """Raw HTTP response JSON"""
    document_type: str
    """Document type"""

    def __init__(
        self,
        doc_config: DocumentConfig,
        http_response: dict,
        pages: List[Document],
        document_type: str,
        document=TypeDocument,
    ):
        """
        Container for the raw API response and the parsed document.

        :param http_response: Raw HTTP response object
        :param pages: List of document objects, page level
        :param document: reconstructed object from all pages
        :param document_type: Document class
        """
        self.http_response = http_response
        self.document_type = document_type
        setattr(self, doc_config.singular_name, document)
        setattr(self, doc_config.plural_name, pages)


def format_response(
    doc_config: DocumentConfig, http_response: dict, input_file
) -> DocumentResponse:
    """
    Create a `DocumentResponse`.

    :param doc_config: DocumentConfig
    :param input_file: Input object
    :param http_response: json response from HTTP call
    :return: Full DocumentResponse object
    """
    http_response["document_type"] = doc_config.document_type
    http_response["input_type"] = input_file.input_type
    http_response["filename"] = input_file.filename
    http_response["filepath"] = input_file.filepath
    http_response["file_extension"] = input_file.file_mimetype
    pages = []

    logger.debug("Handling API response")

    # Create page level objects
    for api_page in http_response["document"]["inference"]["pages"]:
        pages.append(
            doc_config.constructor(
                api_prediction=api_page["prediction"],
                input_file=input_file,
                page_n=api_page["id"],
                document_type=doc_config.document_type,
            )
        )
    # Create the document level object
    document_level = doc_config.constructor(
        api_prediction=http_response["document"]["inference"]["prediction"],
        input_file=input_file,
        document_type=doc_config.document_type,
        page_n=None,
    )
    return DocumentResponse(
        doc_config,
        http_response=http_response,
        pages=pages,
        document_type=doc_config.document_type,
        document=document_level,
    )
