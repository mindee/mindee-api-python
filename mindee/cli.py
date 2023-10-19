import json
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from typing import Dict, Generic, Optional, Type, Union

from mindee import product
from mindee.client import Client, Endpoint
from mindee.error.mindee_error import MindeeClientError
from mindee.input.page_options import PageOptions
from mindee.input.sources import LocalInputSource, UrlInputSource
from mindee.parsing.common.async_predict_response import AsyncPredictResponse
from mindee.parsing.common.document import Document, serialize_for_json
from mindee.parsing.common.feedback_response import FeedbackResponse
from mindee.parsing.common.inference import Inference, TypeInference
from mindee.parsing.common.predict_response import PredictResponse
from mindee.parsing.common.string_dict import StringDict


@dataclass
class CommandConfig(Generic[TypeInference]):
    """Configuration for a command."""

    help: str
    doc_class: Type[TypeInference]
    is_sync: bool = False
    is_async: bool = False


DOCUMENTS: Dict[str, CommandConfig] = {
    "barcode-reader": CommandConfig(
        help="Barcode-reader tool",
        doc_class=product.BarcodeReaderV1,
        is_sync=True,
    ),
    "cropper": CommandConfig(
        help="Cropper tool",
        doc_class=product.CropperV1,
        is_sync=True,
    ),
    "custom": CommandConfig(
        help="Custom document type from API builder",
        doc_class=product.CustomV1,
        is_sync=True,
        is_async=True,
    ),
    "eu-license-plate": CommandConfig(
        help="EU License Plate",
        doc_class=product.eu.LicensePlateV1,
        is_sync=True,
    ),
    "financial-document": CommandConfig(
        help="Financial Document (receipt or invoice)",
        doc_class=product.FinancialDocumentV1,
        is_sync=True,
    ),
    "fr-bank-account-details": CommandConfig(
        help="FR Bank Account Details",
        doc_class=product.fr.BankAccountDetailsV2,
        is_sync=True,
    ),
    "fr-carte-grise": CommandConfig(
        help="FR Carte Grise",
        doc_class=product.fr.CarteGriseV1,
    ),
    "fr-carte-vitale": CommandConfig(
        help="FR Carte Vitale",
        doc_class=product.fr.CarteVitaleV1,
        is_sync=True,
    ),
    "fr-id-card": CommandConfig(
        help="FR ID Card",
        doc_class=product.fr.IdCardV2,
        is_sync=True,
    ),
    "fr-petrol-receipt": CommandConfig(
        help="FR Petrol Receipt",
        doc_class=product.fr.PetrolReceiptV1,
        is_sync=True,
    ),
    "invoice": CommandConfig(
        help="Invoice",
        doc_class=product.InvoiceV4,
        is_sync=True,
    ),
    "invoice-splitter": CommandConfig(
        help="Invoice Splitter",
        doc_class=product.InvoiceSplitterV1,
        is_async=True,
    ),
    "material-certificate": CommandConfig(
        help="Material Certificate",
        doc_class=product.MaterialCertificateV1,
        is_sync=True,
        is_async=True,
    ),
    "multi-receipts": CommandConfig(
        help="Multi-receipts detector",
        doc_class=product.MultiReceiptsDetectorV1,
        is_sync=True,
    ),
    "passport": CommandConfig(
        help="Passport",
        doc_class=product.PassportV1,
        is_sync=True,
    ),
    "proof-of-address": CommandConfig(
        help="Proof of Address",
        doc_class=product.ProofOfAddressV1,
        is_sync=True,
    ),
    "receipt": CommandConfig(
        help="Expense Receipt",
        doc_class=product.ReceiptV5,
        is_sync=True,
    ),
    "us-bank-check": CommandConfig(
        help="US Bank Check",
        doc_class=product.us.BankCheckV1,
        is_sync=True,
    ),
    "us-driver-license": CommandConfig(
        help="US Driver License",
        doc_class=product.us.DriverLicenseV1,
        is_sync=True,
    ),
    "us-w9": CommandConfig(
        help="US W9",
        doc_class=product.us.W9V1,
        is_sync=True,
    ),
}


class MindeeParser:
    """Custom parser for the Mindee CLI."""

    parser: ArgumentParser
    """Parser options."""
    parsed_args: Namespace
    """Stores attributes relating to parsing."""
    client: Client
    """Mindee client"""
    document_info: CommandConfig
    """Config of the document."""
    input_doc: Union[LocalInputSource, UrlInputSource]
    """Document to be parsed."""
    product_class: Type[Inference]
    """Product to parse."""
    feedback: Optional[StringDict]
    """Dict representation of a feedback."""

    def __init__(
        self,
        parser: Optional[ArgumentParser] = None,
        parsed_args: Optional[Namespace] = None,
        client: Optional[Client] = None,
        document_info: Optional[CommandConfig] = None,
    ) -> None:
        self.parser = parser if parser else ArgumentParser(description="Mindee_API")
        self.parsed_args = parsed_args if parsed_args else self._set_args()
        self.client = (
            client
            if client
            else Client(
                api_key=self.parsed_args.api_key
                if "api_key" in self.parsed_args
                else None
            )
        )
        self._set_input()
        self.document_info = (
            document_info if document_info else DOCUMENTS[self.parsed_args.product_name]
        )

    def call_endpoint(self) -> None:
        """Calls the proper type of endpoint according to given command."""
        if self.parsed_args.parse_type == "parse":
            self.call_parse()
        else:
            self.call_feedback()

    def call_feedback(self) -> None:
        """Sends feedback to an API."""
        custom_endpoint: Optional[Endpoint] = None
        if self.parsed_args.product_name == "custom":
            custom_endpoint = self.client.create_endpoint(
                self.parsed_args.endpoint_name,
                self.parsed_args.account_name,
                self.parsed_args.api_version,
            )
        if self.feedback is None:
            raise MindeeClientError("Invalid feedback provided.")

        response: FeedbackResponse = self.client.send_feedback(
            self.document_info.doc_class,
            self.parsed_args.document_id,
            {"feedback": self.feedback},
            custom_endpoint,
        )
        print(json.dumps(response.feedback, indent=2))

    def call_parse(self) -> None:
        """Calls an endpoint with the appropriate method, and displays the results."""
        response: Union[PredictResponse, AsyncPredictResponse]
        if self.document_info.is_sync:
            if self.document_info.is_async:
                if (
                    self.parsed_args.async_parse is not None
                    and self.parsed_args.async_parse
                ):
                    response = self._parse_async()
                else:
                    response = self._parse_sync()
            else:
                response = self._parse_sync()
        else:
            if self.document_info.is_async:
                response = self._parse_async()
            else:
                response = self._parse_sync()

        if self.parsed_args.output_type == "raw":
            print(response.raw_http)
        else:
            if response.document is None:
                raise MindeeClientError("Something went wrong during async parsing.")
            print(self._doc_str(self.parsed_args.output_type, response.document))

    def _parse_sync(self) -> PredictResponse:
        """Processes the results of a synchronous request."""
        page_options: Optional[PageOptions] = None
        if self.parsed_args.cut_doc and self.parsed_args.doc_pages:
            page_options = PageOptions(
                range(self.parsed_args.doc_pages), on_min_pages=0
            )
        custom_endpoint: Optional[Endpoint] = None
        if self.parsed_args.product_name == "custom":
            custom_endpoint = self.client.create_endpoint(
                self.parsed_args.endpoint_name,
                self.parsed_args.account_name,
                self.parsed_args.api_version,
            )
        return self.client.parse(
            self.document_info.doc_class,
            self.input_doc,
            self.parsed_args.include_words,
            page_options=page_options,
            endpoint=custom_endpoint,
        )

    def _parse_async(self) -> AsyncPredictResponse:
        """Enqueues and processes the results of an asynchronous request."""
        page_options: Optional[PageOptions] = None
        if self.parsed_args.cut_doc and self.parsed_args.doc_pages:
            page_options = PageOptions(
                range(self.parsed_args.doc_pages), on_min_pages=0
            )
        custom_endpoint: Optional[Endpoint] = None
        if self.parsed_args.product_name == "custom":
            custom_endpoint = self.client.create_endpoint(
                self.parsed_args.endpoint_name,
                self.parsed_args.account_name,
                self.parsed_args.api_version,
            )
        return self.client.enqueue_and_parse(
            self.document_info.doc_class,
            self.input_doc,
            self.parsed_args.include_words,
            page_options=page_options,
            endpoint=custom_endpoint,
        )

    def _doc_str(self, output_type: str, doc_response: Document) -> str:
        if output_type == "parsed":
            return json.dumps(doc_response, indent=2, default=serialize_for_json)
        return str(doc_response)

    def _set_args(self) -> Namespace:
        """Parse command line arguments."""
        parse_product_subparsers = self.parser.add_subparsers(
            dest="product_name",
            required=True,
        )

        for name, info in DOCUMENTS.items():
            parse_subparser = parse_product_subparsers.add_parser(name, help=info.help)

            call_parser = parse_subparser.add_subparsers(
                dest="parse_type", required=True
            )
            parse_subp = call_parser.add_parser("parse")
            feedback_subp = call_parser.add_parser("feedback")

            self._add_main_options(parse_subp)
            self._add_sending_options(parse_subp)
            self._add_display_options(parse_subp)
            if name == "custom":
                self._add_custom_options(parse_subp)
            else:
                parse_subp.add_argument(
                    "-t",
                    "--full-text",
                    dest="include_words",
                    action="store_true",
                    help="include full document text in response",
                )

            if info.is_async and info.is_sync:
                parse_subp.add_argument(
                    "-A",
                    "--asynchronous",
                    dest="async_parse",
                    help="Parse asynchronously",
                    action="store_true",
                    required=False,
                    default=False,
                )

            self._add_main_options(feedback_subp)
            self._add_feedback_options(feedback_subp)

        parsed_args = self.parser.parse_args()
        return parsed_args

    def _add_main_options(self, parser: ArgumentParser) -> None:
        """
        Adds main options for most parsings.

        :param parser: current parser.
        """
        parser.add_argument(
            "-k",
            "--key",
            dest="api_key",
            help="API key for the account",
            required=False,
            default=None,
        )

    def _add_display_options(self, parser: ArgumentParser) -> None:
        """
        Adds options related to output/display of a document (parse, parse-queued).

        :param parser: current parser.
        """
        parser.add_argument(
            "-o",
            "--output-type",
            dest="output_type",
            choices=["summary", "raw", "parsed"],
            default="summary",
            help="Specify how to output the data.\n"
            "- summary: a basic summary (default)\n"
            "- raw: the raw HTTP response\n"
            "- parsed: the validated and parsed data fields\n",
        )

    def _add_sending_options(self, parser: ArgumentParser) -> None:
        """
        Adds options for sending requests (parse, enqueue).

        :param parser: current parser.
        """
        parser.add_argument(
            "-i",
            "--input-type",
            dest="input_type",
            choices=["path", "file", "base64", "bytes", "url"],
            default="path",
            help="Specify how to handle the input.\n"
            "- path: open a path (default).\n"
            "- file: open as a file handle.\n"
            "- base64: open a base64 encoded text file.\n"
            "- bytes: open the contents as raw bytes.\n"
            "- url: open an URL.",
        )
        parser.add_argument(
            "-c",
            "--cut-doc",
            dest="cut_doc",
            action="store_true",
            help="Cut document pages",
        )
        parser.add_argument(
            "-p",
            "--pages-keep",
            dest="doc_pages",
            type=int,
            default=5,
            help="Number of document pages to keep, default: 5",
        )
        parser.add_argument(dest="path", help="Full path to the file")

    def _add_feedback_options(self, parser: ArgumentParser):
        """
        Adds the option to give feedback manually.

        :param parser: current parser.
        """
        parser.add_argument(
            dest="document_id",
            help="Mindee UUID of the document.",
            type=str,
        )
        parser.add_argument(
            dest="feedback",
            type=json.loads,
            help='Feedback JSON string to send, ex \'{"key": "value"}\'.',
        )

    def _add_custom_options(self, parser: ArgumentParser):
        """
        Adds options to custom-type documents.

        :param parser: current parser.
        """
        parser.add_argument(
            "-a",
            "--account",
            dest="account_name",
            required=True,
            help="API account name for the endpoint (required)",
        )
        parser.add_argument(
            "-e",
            "--endpoint",
            dest="endpoint_name",
            help="API endpoint name (required)",
            required=True,
        )
        parser.add_argument(
            "-v",
            "--version",
            default="1",
            dest="api_version",
            help="Version for the endpoint. If not set, use the latest version of the model.",
        )

    def _get_input_doc(self) -> Union[LocalInputSource, UrlInputSource]:
        """Loads an input document."""
        if self.parsed_args.input_type == "file":
            with open(self.parsed_args.path, "rb", buffering=30) as file_handle:
                return self.client.source_from_file(file_handle)
        elif self.parsed_args.input_type == "base64":
            with open(self.parsed_args.path, "rt", encoding="ascii") as base64_handle:
                return self.client.source_from_b64string(
                    base64_handle.read(), "test.jpg"
                )
        elif self.parsed_args.input_type == "bytes":
            with open(self.parsed_args.path, "rb") as bytes_handle:
                return self.client.source_from_bytes(
                    bytes_handle.read(), bytes_handle.name
                )
        elif self.parsed_args.input_type == "url":
            return self.client.source_from_url(self.parsed_args.path)
        return self.client.source_from_path(self.parsed_args.path)

    def _get_feedback_doc(self) -> StringDict:
        """Loads a feedback."""
        json_doc: StringDict = {}
        if self.parsed_args.input_type == "file":
            with open(self.parsed_args.path, "rb", buffering=30) as f_f:
                json_doc = json.loads(f_f.read())
        elif self.parsed_args.input_type == "base64":
            with open(self.parsed_args.path, "rt", encoding="ascii") as f_b64:
                json_doc = json.loads(f_b64.read())
        elif self.parsed_args.input_type == "bytes":
            with open(self.parsed_args.path, "rb") as f_b:
                json_doc = json.loads(f_b.read())
        else:
            if (
                not self.parsed_args.feedback
                or not "feedback" in self.parsed_args.feedback
            ):
                raise MindeeClientError("Invalid feedback.")
        if not json_doc or "feedback" not in json_doc:
            raise MindeeClientError("Invalid feedback.")
        return json_doc

    def _set_input(self) -> None:
        """Loads an input document, or a feedback document."""
        self.feedback = None
        if self.parsed_args.parse_type == "feedback":
            if not self.parsed_args.feedback:
                self.feedback = self._get_feedback_doc()
            else:
                self.feedback = self.parsed_args.feedback
        else:
            self.input_doc = self._get_input_doc()


def main() -> None:
    """Run the Command Line Interface."""
    parser = MindeeParser()
    parser.call_endpoint()
