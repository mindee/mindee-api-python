import json
from typing import Dict

from mindee.document_config import DocumentConfig, DocumentConfigDict
from mindee.documents.custom_document import CustomDocument
from mindee.documents.financial_document import FinancialDocument
from mindee.documents.invoice import Invoice
from mindee.documents.passport import Passport
from mindee.documents.receipt import Receipt
from mindee.http import (
    CustomEndpoint,
    HTTPException,
    InvoiceEndpoint,
    PassportEndpoint,
    ReceiptEndpoint,
)
from mindee.inputs import (
    Base64Document,
    BytesDocument,
    FileDocument,
    InputDocument,
    PathDocument,
)
from mindee.logger import logger
from mindee.response import DocumentResponse, format_response


class DocumentClient:
    input_doc: InputDocument
    doc_configs: DocumentConfigDict
    raise_on_error: bool = True

    def __init__(
        self,
        input_doc: InputDocument,
        doc_configs: DocumentConfigDict,
        raise_on_error: bool,
    ):
        self.raise_on_error = raise_on_error
        self.doc_configs = doc_configs
        self.input_doc = input_doc

    def parse(
        self,
        document_type: str,
        username: str = None,
        include_words: bool = False,
        close_file: bool = True,
    ) -> DocumentResponse:
        """
        Call prediction API on the document and parse the results.

        :param document_type: Document type to parse
        :param username: API username, the endpoint owner
        :param include_words: Extract all words into http_response
        :param close_file: Whether to `close()` the file after parsing it.
            Set to `False` if you need to access the file after this operation.
        """
        logger.debug("Parsing document as '%s'", document_type)

        found = []
        for k in self.doc_configs.keys():
            if k[1] == document_type:
                found.append(k)

        if len(found) == 0:
            raise RuntimeError(f"Unknown document type: {document_type}")

        if not username:
            if len(found) == 1:
                config_key = found[0]
            else:
                usernames = [k[0] for k in found]
                raise RuntimeError(
                    (
                        "Duplicate configuration detected.\n"
                        f"You specified a document_type '{document_type}' in your custom config.\n"
                        "To avoid confusion, please add the 'account_name' attribute to "
                        f"the parse method, one of {usernames}."
                    )
                )
        else:
            config_key = (username, document_type)

        doc_config = self.doc_configs[config_key]
        for endpoint in doc_config.endpoints:
            if not endpoint.api_key:
                raise RuntimeError(
                    (
                        f"Missing API key for '{endpoint.key_name}',"
                        "check your Client configuration.\n"
                        "You can set this using the "
                        f"'{endpoint.envvar_key_name}' environment variable."
                    )
                )
        return self._make_request(doc_config, include_words, close_file)

    def _make_request(
        self, doc_config: DocumentConfig, include_words: bool, close_file: bool
    ) -> DocumentResponse:
        response = doc_config.constructor.request(
            doc_config.endpoints,
            self.input_doc,
            include_words=include_words,
            close_file=close_file,
        )

        dict_response = response.json()

        if not response.ok and self.raise_on_error:
            raise HTTPException(
                "API %s HTTP error: %s"
                % (response.status_code, json.dumps(dict_response))
            )
        if not response.ok:
            return DocumentResponse(
                doc_config,
                http_response=dict_response,
                pages=[],
                document_type=doc_config.document_type,
                document=None,
            )
        return format_response(
            doc_config, dict_response, doc_config.document_type, self.input_doc
        )

    def close(self) -> None:
        """Close the file object."""
        self.input_doc.file_object.close()


class Client:
    """
    Mindee API Client.

    See: https://developers.mindee.com/docs/
    """

    _doc_configs: DocumentConfigDict
    raise_on_error: bool = True

    def __init__(self, raise_on_error: bool = True):
        """
        Mindee API Client.

        :param raise_on_error: Raise an Exception on HTTP errors
        """
        self._doc_configs: Dict[tuple, DocumentConfig] = {}
        self.raise_on_error = raise_on_error

    def config_custom_doc(
        self,
        document_type: str,
        singular_name: str,
        plural_name: str,
        account_name: str,
        api_key: str = "",
        version: str = "1",
    ):
        """
        Configure a custom document using the Mindee API Builder.

        :param document_type: The "document type" field in the "Settings" page of the API Builder
        :param singular_name: The name of the attribute used to retrieve
            a *single* document from the API response
        :param plural_name: The name of the attribute used to retrieve
            *multiple* documents from the API response
        :param account_name: Your organization's username on the API Builder
        :param api_key: Your API key for the endpoint
        :param version: If set, locks the version of the model to use.
                        If not set, use the latest version of the model.
        """
        self._doc_configs[(account_name, document_type)] = DocumentConfig(
            document_type=document_type,
            singular_name=singular_name,
            plural_name=plural_name,
            constructor=CustomDocument,
            endpoints=[
                CustomEndpoint(
                    owner=account_name,
                    url_name=document_type,
                    version=version,
                    api_key=api_key,
                ),
            ],
        )
        return self

    def config_invoice(self, api_key: str = None):
        """
        Configure a Mindee Invoice document.

        :param api_key: Invoice API key
        """
        config = DocumentConfig(
            document_type="invoice",
            singular_name="invoice",
            plural_name="invoices",
            constructor=Invoice,
            endpoints=[InvoiceEndpoint(api_key=api_key)],
        )
        self._doc_configs[("mindee", "invoice")] = config
        return self

    def config_receipt(self, api_key: str = None):
        """
        Configure a Mindee Expense Receipts document.

        :param api_key: Expense Receipt API key
        """
        config = DocumentConfig(
            document_type="receipt",
            singular_name="receipt",
            plural_name="receipts",
            constructor=Receipt,
            endpoints=[ReceiptEndpoint(api_key=api_key)],
        )
        self._doc_configs[("mindee", "receipt")] = config
        return self

    def config_financial_doc(
        self, invoice_api_key: str = None, receipt_api_key: str = None
    ):
        """
        Configure a Mindee Financial document. Uses Invoice and Expense Receipt internally.

        :param receipt_api_key: Expense Receipt API key
        :param invoice_api_key: Invoice API key
        """
        config = DocumentConfig(
            document_type="financial_doc",
            singular_name="financial_doc",
            plural_name="financial_docs",
            constructor=FinancialDocument,
            endpoints=[
                InvoiceEndpoint(api_key=invoice_api_key),
                ReceiptEndpoint(api_key=receipt_api_key),
            ],
        )
        self._doc_configs[("mindee", "financial_doc")] = config
        return self

    def config_passport(self, api_key: str = None):
        """
        Configure a Mindee Passport document.

        :param api_key: Passport API key
        """
        config = DocumentConfig(
            document_type="passport",
            singular_name="passport",
            plural_name="passports",
            constructor=Passport,
            endpoints=[PassportEndpoint(api_key=api_key)],
        )
        self._doc_configs[("mindee", "passport")] = config
        return self

    def doc_from_path(
        self,
        input_path: str,
        cut_pdf: bool = True,
        cut_pdf_mode: int = 3,
    ) -> DocumentClient:
        """
        Load a document from an absolute path, as a string.

        :param input_path: Path of file to open
        :param cut_pdf_mode: Number (between 1 and 3 incl.) of pages to reconstruct a pdf with.

            * if 1: pages [0]
            * if 2: pages [0, n-2]
            * if 3: pages [0, n-2, n-1]
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        """
        input_doc = PathDocument(input_path, cut_pdf=cut_pdf, n_pdf_pages=cut_pdf_mode)
        return DocumentClient(
            input_doc=input_doc,
            doc_configs=self._doc_configs,
            raise_on_error=self.raise_on_error,
        )

    def doc_from_file(
        self,
        input_file,
        cut_pdf: bool = True,
        cut_pdf_mode: int = 3,
    ) -> DocumentClient:
        """
        Load a document from a normal Python file object/handle.

        :param input_file: Input file handle
        :param cut_pdf_mode: Number (between 1 and 3 incl.) of pages to reconstruct a pdf with.

            * if 1: pages [0]
            * if 2: pages [0, n-2]
            * if 3: pages [0, n-2, n-1]
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        """
        input_doc = FileDocument(
            input_file,
            cut_pdf=cut_pdf,
            n_pdf_pages=cut_pdf_mode,
        )
        return DocumentClient(
            input_doc=input_doc,
            doc_configs=self._doc_configs,
            raise_on_error=self.raise_on_error,
        )

    def doc_from_b64string(
        self,
        input_string: str,
        filename: str,
        cut_pdf: bool = True,
        cut_pdf_mode: int = 3,
    ) -> DocumentClient:
        """
        Load a document from a base64 encoded string.

        :param input_string: Input to parse as base64 string
        :param filename: The name of the file (without the path)
        :param cut_pdf_mode: Number (between 1 and 3 incl.) of pages to reconstruct a pdf with.

            * if 1: pages [0]
            * if 2: pages [0, n-2]
            * if 3: pages [0, n-2, n-1]
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        """
        input_doc = Base64Document(
            input_string,
            filename,
            cut_pdf=cut_pdf,
            n_pdf_pages=cut_pdf_mode,
        )
        return DocumentClient(
            input_doc=input_doc,
            doc_configs=self._doc_configs,
            raise_on_error=self.raise_on_error,
        )

    def doc_from_bytes(
        self,
        input_bytes: bytes,
        filename: str,
        cut_pdf: bool = True,
        cut_pdf_mode: int = 3,
    ) -> DocumentClient:
        """
        Load a document from raw bytes.

        :param input_bytes: Raw byte input
        :param filename: The name of the file (without the path)
        :param cut_pdf_mode: Number (between 1 and 3 incl.) of pages to reconstruct a PDF with.

            * if 1: pages [0]
            * if 2: pages [0, n-2]
            * if 3: pages [0, n-2, n-1]
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        """
        input_doc = BytesDocument(
            input_bytes,
            filename,
            cut_pdf=cut_pdf,
            n_pdf_pages=cut_pdf_mode,
        )
        return DocumentClient(
            input_doc=input_doc,
            doc_configs=self._doc_configs,
            raise_on_error=self.raise_on_error,
        )
