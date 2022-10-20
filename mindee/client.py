import json
from typing import BinaryIO, Dict, Optional

from mindee.document_config import DocumentConfig, DocumentConfigDict
from mindee.documents.bank_check import BankCheck
from mindee.documents.custom_document import CustomDocument
from mindee.documents.financial_document import FinancialDocument
from mindee.documents.invoice import Invoice
from mindee.documents.passport import Passport
from mindee.documents.receipt import Receipt
from mindee.endpoints import (
    OTS_OWNER,
    BankCheckEndpoint,
    CustomEndpoint,
    HTTPException,
    InvoiceEndpoint,
    PassportEndpoint,
    ReceiptEndpoint,
)
from mindee.input.page_options import PageOptions
from mindee.input.sources import (
    Base64Input,
    BytesInput,
    FileInput,
    InputSource,
    PathInput,
)
from mindee.logger import logger
from mindee.response import PredictResponse


class DocumentClient:
    input_doc: InputSource
    doc_configs: DocumentConfigDict
    raise_on_error: bool = True

    def __init__(
        self,
        input_doc: InputSource,
        doc_configs: DocumentConfigDict,
        raise_on_error: bool,
    ):
        self.raise_on_error = raise_on_error
        self.doc_configs = doc_configs
        self.input_doc = input_doc

    def parse(
        self,
        document_type: str,
        username: Optional[str] = None,
        include_words: bool = False,
        close_file: bool = True,
        page_options: Optional[PageOptions] = None,
    ) -> PredictResponse:
        """
        Call prediction API on the document and parse the results.

        :param document_type: Document type to parse
        :param username: API username, the endpoint owner
        :param include_words: Include all the words of the document in the response
        :param close_file: Whether to `close()` the file after parsing it.
            Set to `False` if you need to access the file after this operation.
        :param page_options: PageOptions object for cutting multipage documents.
        """
        logger.debug("Parsing document as '%s'", document_type)

        found = []
        for k in self.doc_configs.keys():
            if k[1] == document_type:
                found.append(k)

        if len(found) == 0:
            raise RuntimeError(f"Document type not configured: {document_type}")

        if username:
            config_key = (username, document_type)
        elif len(found) == 1:
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

        doc_config = self.doc_configs[config_key]
        doc_config.check_api_keys()
        if page_options and self.input_doc.is_pdf():
            self.input_doc.process_pdf(
                page_options.behavior,
                page_options.on_min_pages,
                page_options.page_indexes,
            )
        return self._make_request(doc_config, include_words, close_file)

    def _make_request(
        self, doc_config: DocumentConfig, include_words: bool, close_file: bool
    ) -> PredictResponse:
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
        return PredictResponse(
            http_response=dict_response,
            doc_config=doc_config,
            input_source=self.input_doc,
            response_ok=response.ok,
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
    raise_on_error: bool
    api_key: str

    def __init__(self, api_key: str = "", raise_on_error: bool = True):
        """
        Mindee API Client.

        :param api_key: Your API key for all endpoints
        :param raise_on_error: Raise an Exception on HTTP errors
        """
        self._doc_configs: Dict[tuple, DocumentConfig] = {}
        self.raise_on_error = raise_on_error
        self.api_key = api_key

    def config_custom_doc(
        self,
        account_name: str,
        endpoint_name: str,
        version: str = "1",
    ) -> "Client":
        """
        Configure a custom document using the Mindee API Builder.

        :param endpoint_name: The "API name" field in the "Settings" page of the API Builder
        :param account_name: Your organization's username on the API Builder
        :param version: If set, locks the version of the model to use.
                        If not set, use the latest version of the model.
        """
        self._doc_configs[(account_name, endpoint_name)] = DocumentConfig(
            document_type=endpoint_name,
            constructor=CustomDocument,
            endpoints=[
                CustomEndpoint(
                    owner=account_name,
                    url_name=endpoint_name,
                    version=version,
                    api_key=self.api_key,
                ),
            ],
        )
        return self

    def config_invoice(self) -> "Client":
        """Configure a Mindee Invoice document."""
        config = DocumentConfig(
            document_type="invoice",
            constructor=Invoice,
            endpoints=[InvoiceEndpoint(api_key=self.api_key)],
        )
        self._doc_configs[(OTS_OWNER, "invoice")] = config
        return self

    def config_receipt(self) -> "Client":
        """Configure a Mindee Expense Receipts document."""
        config = DocumentConfig(
            document_type="receipt",
            constructor=Receipt,
            endpoints=[ReceiptEndpoint(api_key=self.api_key)],
        )
        self._doc_configs[(OTS_OWNER, "receipt")] = config
        return self

    def config_financial_doc(
        self,
    ) -> "Client":
        """Configure a Mindee Financial document. Uses Invoice and Expense Receipt internally."""
        config = DocumentConfig(
            document_type="financial_doc",
            constructor=FinancialDocument,
            endpoints=[
                InvoiceEndpoint(api_key=self.api_key),
                ReceiptEndpoint(api_key=self.api_key),
            ],
        )
        self._doc_configs[(OTS_OWNER, "financial_doc")] = config
        return self

    def config_passport(self) -> "Client":
        """Configure a Mindee Passport document."""
        config = DocumentConfig(
            document_type="passport",
            constructor=Passport,
            endpoints=[PassportEndpoint(api_key=self.api_key)],
        )
        self._doc_configs[(OTS_OWNER, "passport")] = config
        return self

    def config_bank_check(self) -> "Client":
        """Configure a Mindee Bank check document."""
        config = DocumentConfig(
            document_type="bank_check",
            constructor=BankCheck,
            endpoints=[BankCheckEndpoint(api_key=self.api_key)],
        )
        self._doc_configs[(OTS_OWNER, "bank_check")] = config
        return self

    def doc_from_path(
        self,
        input_path: str,
    ) -> DocumentClient:
        """
        Load a document from an absolute path, as a string.

        :param input_path: Path of file to open
        """
        input_doc = PathInput(input_path)
        return DocumentClient(
            input_doc=input_doc,
            doc_configs=self._doc_configs,
            raise_on_error=self.raise_on_error,
        )

    def doc_from_file(
        self,
        input_file: BinaryIO,
    ) -> DocumentClient:
        """
        Load a document from a normal Python file object/handle.

        :param input_file: Input file handle
        """
        input_doc = FileInput(
            input_file,
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
    ) -> DocumentClient:
        """
        Load a document from a base64 encoded string.

        :param input_string: Input to parse as base64 string
        :param filename: The name of the file (without the path)
        """
        input_doc = Base64Input(
            input_string,
            filename,
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
    ) -> DocumentClient:
        """
        Load a document from raw bytes.

        :param input_bytes: Raw byte input
        :param filename: The name of the file (without the path)
        """
        input_doc = BytesInput(
            input_bytes,
            filename,
        )
        return DocumentClient(
            input_doc=input_doc,
            doc_configs=self._doc_configs,
            raise_on_error=self.raise_on_error,
        )
