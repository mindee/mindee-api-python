import os
import json
from typing import Optional, List, Dict, Any

import requests

from mindee.http import HTTPException
from mindee.inputs import Inputs
from mindee.documents import DOCUMENT_CONFIGS
from mindee.documents.base import OFF_THE_SHELF
from mindee.documents.custom_document import CustomDocument

from mindee.documents.document_config import DocumentConfig, validate_list


class Client:
    documents = DOCUMENT_CONFIGS

    def __init__(
        self,
        receipt_api_key: Optional[str] = None,
        invoice_api_key: Optional[str] = None,
        passport_api_key: Optional[str] = None,
        custom_documents: Optional[List[dict]] = None,
        raise_on_error: bool = True,
    ):
        """
        :param receipt_api_key: expense_receipt Mindee API token, see https://mindee.com
        :param custom_documents: (list<dict>), List of custom endpoint configuration dictionnaries
        :param invoice_api_key: invoice Mindee API token, see https://mindee.com
        :param passport_api_key: passport Mindee API token, see https://mindee.com
        :param raise_on_error: (bool, default True) raise an Exception on HTTP errors
        """
        self.raise_on_error = raise_on_error

        self.receipt_api_key = receipt_api_key
        self.invoice_api_key = invoice_api_key
        self.passport_api_key = passport_api_key
        self._set_api_keys_from_env()

        # Build custom document configs from Client custom_document kwarg
        if custom_documents is not None:
            for custom_document_cfg in custom_documents:
                assert "document_type" in custom_document_cfg.keys()
                assert custom_document_cfg["document_type"] not in self.documents.keys()
                self.documents[custom_document_cfg["document_type"]] = DocumentConfig(
                    custom_document_cfg
                )
        validate_list(self.documents)

    def _get_api_key(self, key_name) -> Optional[str]:
        return getattr(self, f"{key_name}_api_key", None)

    def _set_api_keys_from_env(self) -> None:
        for doc_config in self.documents.values():
            for key_name in doc_config.required_ots_keys:
                if not self._get_api_key(key_name):
                    val = os.getenv(f"MINDEE_{key_name.upper()}_API_KEY", None)
                    setattr(self, f"{key_name}_api_key", val)

    def parse_from_path(
        self,
        input_path: str,
        document_type: str,
        cut_pdf: bool = True,
        cut_pdf_mode: int = 3,
        include_words=False,
    ):
        """
        :param input_path: Path of file to open
        :param document_type: Document type to parse
        :param cut_pdf_mode: Number (between 1 and 3 incl.) of pages to reconstruct a pdf with.
                        if 1: pages [0]
                        if 2: pages [0, n-2]
                        if 3: pages [0, n-2, n-1]
        :param include_words: Bool, extract all words into http_response
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        :return: Wrapped response with Receipts objects parsed
        """
        self._validate_arguments(document_type)
        input_file = Inputs(
            input_path, "path", cut_pdf=cut_pdf, n_pdf_pages=cut_pdf_mode
        )
        return self._make_request(
            input_file, document_type, include_words=include_words
        )

    def parse_from_file(
        self,
        input_file,
        document_type: str,
        cut_pdf: bool = True,
        cut_pdf_mode: int = 3,
        include_words=False,
    ):
        """
        :param input_file: Input file handle
        :param document_type: Document type to parse
        :param cut_pdf_mode: Number (between 1 and 3 incl.) of pages to reconstruct a pdf with.
                        if 1: pages [0]
                        if 2: pages [0, n-2]
                        if 3: pages [0, n-2, n-1]
        :param include_words: Bool, extract all words into http_response
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        :return: Wrapped response with Receipts objects parsed
        """
        self._validate_arguments(document_type)
        input_file = Inputs(
            input_file,
            "file",
            cut_pdf=cut_pdf,
            n_pdf_pages=cut_pdf_mode,
        )
        return self._make_request(
            input_file, document_type, include_words=include_words
        )

    def parse_from_b64string(
        self,
        input_string: str,
        filename: str,
        document_type: str,
        cut_pdf: bool = True,
        cut_pdf_mode: int = 3,
        include_words=False,
    ):
        """
        :param input_string: Input to parse as base64 string
        :param filename: The name of the file (without the path)
        :param document_type: Document type to parse
        :param cut_pdf_mode: Number (between 1 and 3 incl.) of pages to reconstruct a pdf with.
                        if 1: pages [0]
                        if 2: pages [0, n-2]
                        if 3: pages [0, n-2, n-1]
        :param include_words: Bool, extract all words into http_response
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        :return: Wrapped response with Receipts objects parsed
        """
        self._validate_arguments(document_type)
        input_file = Inputs(
            input_string,
            "base64",
            filename=filename,
            cut_pdf=cut_pdf,
            n_pdf_pages=cut_pdf_mode,
        )
        return self._make_request(
            input_file, document_type, include_words=include_words
        )

    def parse_from_bytes(
        self,
        input_bytes,
        filename: str,
        document_type: str,
        cut_pdf: bool = True,
        cut_pdf_mode: int = 3,
        include_words=False,
    ):
        """
        :param input_bytes: Raw byte input
        :param document_type: Document type to parse
        :param filename: The name of the file (without the path)
        :param cut_pdf_mode: Number (between 1 and 3 incl.) of pages to reconstruct a pdf with.
                        if 1: pages [0]
                        if 2: pages [0, n-2]
                        if 3: pages [0, n-2, n-1]
        :param include_words: Bool, extract all words into http_response
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        :return: Wrapped response with Receipts objects parsed
        """
        self._validate_arguments(document_type)
        input_file = Inputs(
            input_bytes,
            "bytes",
            filename=filename,
            cut_pdf=cut_pdf,
            n_pdf_pages=cut_pdf_mode,
        )
        return self._make_request(
            input_file, document_type, include_words=include_words
        )

    def _validate_arguments(self, document_type: str):
        # first let's validate the document type
        if document_type not in self.documents.keys():
            raise AssertionError(
                f"{document_type} document type was not found in document configurations"
            )
        if self.documents[document_type].type == OFF_THE_SHELF:
            for api_key_name in self.documents[document_type].required_ots_keys:
                if not self._get_api_key(api_key_name):
                    raise AssertionError(
                        f"Missing API key for '{api_key_name}', check your Client configuration."
                    )

    def _make_request(self, input_file, document_type: str, include_words=False):
        doc_config = self.documents[document_type]
        if doc_config.type == OFF_THE_SHELF:
            response = doc_config.constructor.request(
                self, input_file, include_words=include_words
            )
        else:
            response = CustomDocument.request(
                input_file,
                document_type,
                doc_config.api_username,
                doc_config.api_key,
                doc_config.interface_version,
            )
        return self._wrap_response(input_file, response, document_type)

    def _wrap_response(
        self, input_file, response: requests.Response, document_type: str
    ):
        """
        :param input_file: Input object
        :param response: HTTP response
        :param document_type: Document class
        :return: Full response object
        """
        dict_response = response.json()

        if response.status_code > 201 and self.raise_on_error:
            raise HTTPException(
                "API %s HTTP error: %s"
                % (response.status_code, json.dumps(dict_response))
            )
        if response.status_code > 201:
            return Response(
                self,
                http_response=dict_response,
                pages=[],
                document_type=document_type,
                document=None,
            )
        return Response.format_response(self, dict_response, document_type, input_file)


class Response:
    http_response: Dict[str, Any]
    document_type: str

    def __init__(
        self,
        client,
        http_response: dict,
        pages: list,
        document_type: str,
        document=None,
    ):
        """
        :param http_response: HTTP response object
        :param pages: List of document objects
        :param document: reconstructed object from all pages
        :param document_type: Document class
        """
        self.http_response = http_response
        self.document_type = document_type
        setattr(self, client.documents[document_type].singular_name, document)
        setattr(self, client.documents[document_type].plural_name, pages)

    @staticmethod
    def format_response(client, http_response, document_type, input_file):
        """
        :param client: Client object
        :param input_file: Input object
        :param http_response: json response from HTTP call
        :param document_type: Document class
        :return: Full Response object
        """
        http_response["document_type"] = document_type
        http_response["input_type"] = input_file.input_type
        http_response["filename"] = input_file.filename
        http_response["filepath"] = input_file.filepath
        http_response["file_extension"] = input_file.file_extension
        pages = []

        if document_type not in client.documents.keys():
            raise Exception("Document type not supported.")

        # Create page level objects
        for _, page_prediction in enumerate(
            http_response["document"]["inference"]["pages"]
        ):
            pages.append(
                client.documents[document_type].constructor(
                    api_prediction=page_prediction["prediction"],
                    input_file=input_file,
                    page_n=page_prediction["id"],
                    document_type=document_type,
                )
            )

        # Create the document level object
        document_level = client.documents[document_type].constructor(
            api_prediction=http_response["document"]["inference"]["prediction"],
            input_file=input_file,
            document_type=document_type,
            page_n="-1",
        )

        return Response(
            client,
            http_response=http_response,
            pages=pages,
            document_type=document_type,
            document=document_level,
        )
