import json

from mindee.inputs import (
    InputDocument,
    Base64Document,
    BytesDocument,
    FileDocument,
    PathDocument,
)
from mindee.response import format_response, DocumentResponse
from mindee.http import HTTPException
from mindee.document_config import DocumentConfig, DocumentConfigDict
from mindee.documents.receipt import Receipt
from mindee.documents.financial_document import FinancialDocument
from mindee.documents.invoice import Invoice
from mindee.documents.passport import Passport


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
        self, document_type: str, username: str = None, include_words: bool = False
    ):
        """
        :param document_type: Document type to parse
        :param username:
        :param include_words: Bool, extract all words into http_response
        """
        if not username:
            found = []
            for k in self.doc_configs.keys():
                if k[1] == document_type:
                    found.append(k)
            if len(found) == 1:
                config_key = found[0]
            else:
                usernames = [k[0] for k in found]
                raise RuntimeError(
                    (
                        "Duplicate configuration detected.\n"
                        f"You specified a document_type '{document_type}' in your custom config.\n"
                        "To avoid confusion, please add the 'account_name' attribute to the parse method, "
                        f"one of {usernames}."
                    )
                )
        else:
            config_key = (username, document_type)

        doc_config = self.doc_configs[config_key]
        for endpoint in doc_config.endpoints:
            if not endpoint.api_key:
                raise RuntimeError(
                    (
                        f"Missing API key for '{endpoint.key_name}', check your Client configuration.\n"
                        f"You can set this using the '{endpoint.envvar_key_name}' environment variable."
                    )
                )
        return self._make_request(doc_config, include_words)

    def _make_request(self, doc_config: DocumentConfig, include_words: bool):
        response = doc_config.constructor.request(
            doc_config.endpoints, self.input_doc, include_words=include_words
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


class Client:
    _doc_configs: DocumentConfigDict
    raise_on_error: bool = True

    def __init__(self, raise_on_error: bool = True):
        """
        :param raise_on_error: Raise an Exception on HTTP errors
        """
        self._doc_configs = {
            ("mindee", "receipt"): Receipt.get_document_config(),
            ("mindee", "invoice"): Invoice.get_document_config(),
            ("mindee", "financial_doc"): FinancialDocument.get_document_config(),
            ("mindee", "passport"): Passport.get_document_config(),
        }
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

        See: https://developers.mindee.com/docs/

        :param document_type: The "document type" field in the "Settings" page of the API Builder
        :param singular_name: The name of the attribute used to retrieve a *single* document from the API response
        :param plural_name: The name of the attribute used to retrieve *multiple* documents from the API response
        :param account_name: Your organization's username on the API Builder
        :param api_key: Your API key for the endpoint
        :param version: If set, locks the version of the model to use.
                        If not set, use the latest version of the model.
        """
        self._doc_configs[(account_name, document_type)] = DocumentConfig(
            {
                "document_type": document_type,
                "singular_name": singular_name,
                "plural_name": plural_name,
                "account_name": account_name,
                "api_key": api_key,
                "interface_version": version,
            }
        )
        return self

    def config_invoice(self, api_key: str = None):
        """
        Configure a Mindee Invoice document.

        See: https://developers.mindee.com/docs/

        :param api_key: Invoice API key
        """
        if api_key:
            self._doc_configs[("mindee", "invoice")].endpoints[0].api_key = api_key
        return self

    def config_receipt(self, api_key: str = None):
        """
        Configure a Mindee Expense Receipts document.

        See: https://developers.mindee.com/docs/

        :param api_key: Expense Receipt API key
        """
        if api_key:
            self._doc_configs[("mindee", "receipt")].endpoints[0].api_key = api_key
        return self

    def config_financial_doc(
        self, invoice_api_key: str = None, receipt_api_key: str = None
    ):
        """
        Configure a Mindee Financial document. Uses Invoice and Expense Receipt internally.

        See: https://developers.mindee.com/docs/

        :param receipt_api_key: Expense Receipt API key
        :param invoice_api_key: Invoice API key
        """
        if invoice_api_key:
            self._doc_configs[("mindee", "financial_doc")].endpoints[
                0
            ].api_key = invoice_api_key
        if receipt_api_key:
            self._doc_configs[("mindee", "financial_doc")].endpoints[
                1
            ].api_key = receipt_api_key
        return self

    def config_passport(self, api_key: str = None):
        """
        Configure a Mindee Passport document.

        See: https://developers.mindee.com/docs/

        :param api_key: Passport API key
        """
        if api_key:
            self._doc_configs[("mindee", "passport")].endpoints[0].api_key = api_key
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
                        if 1: pages [0]
                        if 2: pages [0, n-2]
                        if 3: pages [0, n-2, n-1]
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        :return: Wrapped response with Receipts objects parsed
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
                        if 1: pages [0]
                        if 2: pages [0, n-2]
                        if 3: pages [0, n-2, n-1]
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        :return: Wrapped response with Receipts objects parsed
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
        :param filename: The url_name of the file (without the path)
        :param cut_pdf_mode: Number (between 1 and 3 incl.) of pages to reconstruct a pdf with.
                        if 1: pages [0]
                        if 2: pages [0, n-2]
                        if 3: pages [0, n-2, n-1]
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        :return: Wrapped response with Receipts objects parsed
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
        :param filename: The url_name of the file (without the path)
        :param cut_pdf_mode: Number (between 1 and 3 incl.) of pages to reconstruct a pdf with.
                        if 1: pages [0]
                        if 2: pages [0, n-2]
                        if 3: pages [0, n-2, n-1]
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        :return: Wrapped response with Receipts objects parsed
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
