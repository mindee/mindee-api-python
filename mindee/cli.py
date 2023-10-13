import json
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from typing import Dict, Generic, Optional, Type, Union

from mindee import product
from mindee.client import Client, Endpoint
from mindee.input.page_options import PageOptions
from mindee.input.sources import LocalInputSource, UrlInputSource
from mindee.parsing.common.async_predict_response import AsyncPredictResponse
from mindee.parsing.common.document import Document, serialize_for_json
from mindee.parsing.common.inference import Inference, TypeInference
from mindee.parsing.common.predict_response import PredictResponse


@dataclass
class CommandConfig(Generic[TypeInference]):
    """Configuration for a command."""

    help: str
    doc_class: TypeInference
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
    "fr-bank-account-details": CommandConfig(
        help="FR Bank Account Details",
        doc_class=product.fr.BankAccountDetailsV2,
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
    """Product to parse"""

    def __init__(self) -> None:
        self.parser = ArgumentParser(description="Mindee_API")
        self.parsed_args = self._set_args()
        self.client = Client(api_key=self.parsed_args.api_key)
        if self.parsed_args.parse_type == "parse":
            self.input_doc = self._get_input_doc()
        self.document_info = DOCUMENTS[self.parsed_args.product_name]

    def call_endpoint(self) -> None:
        """Calls the proper type of endpoint according to given command."""
        if self.parsed_args.parse_type == "parse":
            self.call_parse()
        else:
            self.call_fetch()

    def call_fetch(self) -> None:
        """Fetches an API's for a previously enqueued document."""
        response: AsyncPredictResponse = self._parse_queued()
        if self.parsed_args.output_type == "raw":
            print(response.raw_http)
        else:
            if not hasattr(response, "document") or response.document is None:
                print(response.job)
            else:
                print(response.document)

    def call_parse(self) -> None:
        """Calls an endpoint with the appropriate method, and displays the results."""
        response: Union[PredictResponse, AsyncPredictResponse]
        if self.document_info.is_sync:
            if self.document_info.is_async:
                if self.parsed_args.async_parse is not None:
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
                raise RuntimeError("Something went wrong during async parsing.")
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
            self.client.create_endpoint(
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
            self.client.create_endpoint(
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

    def _parse_queued(self) -> AsyncPredictResponse:
        """Fetches a queue's result from a document's id."""
        custom_endpoint: Optional[Endpoint] = None
        if self.parsed_args.product_name == "custom":
            self.client.create_endpoint(
                self.parsed_args.endpoint_name,
                self.parsed_args.account_name,
                self.parsed_args.api_version,
            )
        return self.client.parse_queued(
            self.document_info.doc_class,
            self.parsed_args.queue_id,
            custom_endpoint,
        )

    def _doc_str(self, output_type: str, doc_response: Document) -> str:
        if output_type == "parsed":
            return json.dumps(doc_response, indent=2, default=serialize_for_json)
        return str(doc_response)

    def _set_args(self) -> Namespace:
        """Parse command line arguments."""
        call_parser = self.parser.add_subparsers(
            dest="parse_type",
            required=True,
        )
        parse_subparser = call_parser.add_parser("parse")
        fetch_subparser = call_parser.add_parser("fetch")

        parse_product_subparsers = parse_subparser.add_subparsers(
            dest="product_name",
            required=True,
        )

        fetch_product_subparsers = fetch_subparser.add_subparsers(
            dest="product_name",
            required=True,
        )

        for name, info in DOCUMENTS.items():
            parse_subp = parse_product_subparsers.add_parser(name, help=info.help)
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
                    required=False,
                    default=False,
                )

            if info.is_async:
                fetch_subp = fetch_product_subparsers.add_parser(name, help=info.help)
                self._add_main_options(fetch_subp)
                self._add_display_options(fetch_subp)
                self._add_fetch_options(fetch_subp)

        parsed_args = self.parser.parse_args()
        return parsed_args

    def _add_main_options(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "-k",
            "--key",
            dest="api_key",
            help="API key for the account",
            required=False,
            default=None,
        )

    def _add_display_options(self, parser: ArgumentParser) -> None:
        """Adds options related to output/display of a document (parse, parse-queued)."""
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
        """Adds options for sending requests (parse, enqueue)."""
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

    def _add_fetch_options(self, parser: ArgumentParser):
        """Adds an option to provide the queue ID for an async document."""
        parser.add_argument(
            dest="queue_id",
            help="Async queue ID for a document (required)",
        )

    def _add_custom_options(self, parser: ArgumentParser):
        """Adds options to custom-type documents."""
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


def main() -> None:
    """Run the Command Line Interface."""
    parser = MindeeParser()
    parser.call_endpoint()
