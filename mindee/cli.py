import argparse
import json
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from typing import Dict, Generic, TypeVar

from mindee import Client, PageOptions, documents
from mindee.client import DocumentClient
from mindee.documents.base import Document, serialize_for_json
from mindee.response import PredictResponse

TypeDoc = TypeVar("TypeDoc", bound=Document)


@dataclass
class CommandConfig(Generic[TypeDoc]):
    """Configuration for a command."""

    help: str
    doc_class: TypeDoc
    is_sync: bool = True
    is_async: bool = False


DOCUMENTS: Dict[str, CommandConfig] = {
    "custom": CommandConfig(
        help="Custom document type from API builder",
        doc_class=documents.TypeCustomV1,
    ),
    "invoice": CommandConfig(
        help="Invoice",
        doc_class=documents.TypeInvoiceV4,
    ),
    "receipt": CommandConfig(
        help="Expense Receipt",
        doc_class=documents.TypeReceiptV5,
    ),
    "passport": CommandConfig(
        help="Passport",
        doc_class=documents.TypePassportV1,
    ),
    "financial-document": CommandConfig(
        help="Financial Document (receipt or invoice)",
        doc_class=documents.TypeFinancialDocumentV1,
    ),
    "proof-of-address": CommandConfig(
        help="Proof of Address",
        doc_class=documents.TypeProofOfAddressV1,
    ),
    "us-bank-check": CommandConfig(
        help="US Bank Check",
        doc_class=documents.us.TypeBankCheckV1,
    ),
    "eu-license-plate": CommandConfig(
        help="EU License Plate",
        doc_class=documents.eu.TypeLicensePlateV1,
    ),
    "fr-carte-grise": CommandConfig(
        help="FR Carte Grise",
        doc_class=documents.fr.TypeCarteGriseV1,
    ),
    "fr-carte-vitale": CommandConfig(
        help="FR Carte Vitale",
        doc_class=documents.fr.TypeCarteVitaleV1,
    ),
    "fr-id-card": CommandConfig(
        help="FR ID Card",
        doc_class=documents.fr.TypeIdCardV1,
    ),
    "fr-bank-account-details": CommandConfig(
        help="FR Bank Account Details",
        doc_class=documents.fr.TypeBankAccountDetailsV1,
    ),
    "invoice-splitter": CommandConfig(
        help="Invoice Splitter",
        doc_class=documents.TypeInvoiceSplitterV1,
        is_sync=False,
        is_async=True,
    ),
}


def _get_input_doc(client: Client, args: Namespace) -> DocumentClient:
    if args.input_type == "file":
        with open(args.path, "rb", buffering=30) as file_handle:
            return client.doc_from_file(input_file=file_handle)
    elif args.input_type == "base64":
        with open(args.path, "rt", encoding="ascii") as base64_handle:
            return client.doc_from_b64string(
                input_string=base64_handle.read(), filename="test.jpg"
            )
    elif args.input_type == "bytes":
        with open(args.path, "rb") as bytes_handle:
            return client.doc_from_bytes(
                input_bytes=bytes_handle.read(), filename=bytes_handle.name
            )
    elif args.input_type == "url":
        return client.doc_from_url(url=args.path)
    return client.doc_from_path(args.path)


def call_endpoint(args: Namespace):
    """Call the endpoint given passed arguments."""
    client = Client(api_key=args.api_key, raise_on_error=args.raise_on_error)
    info = DOCUMENTS[args.product_name]
    doc_class = info.doc_class

    if args.call_method == "enqueue":
        process_parse_enqueue(args, client, doc_class)
    elif args.call_method == "parse-queued":
        process_parse_queued(args, client, doc_class)
    elif args.call_method == "parse":
        process_parse(args, client, doc_class)


def process_parse(args: Namespace, client: Client, doc_class) -> None:
    """Processes the results of a parsing request."""
    if args.cut_doc and args.doc_pages:
        page_options = PageOptions(range(args.doc_pages), on_min_pages=0)
    else:
        page_options = None
    input_doc = _get_input_doc(client, args)
    if args.product_name == "custom":
        client.add_endpoint(
            endpoint_name=args.endpoint_name,
            account_name=args.account_name,
            version=args.api_version,
        )
        parsed_data = input_doc.parse(
            doc_class,
            endpoint_name=args.endpoint_name,
            account_name=args.account_name,
            page_options=page_options,
        )
    else:
        parsed_data = input_doc.parse(
            doc_class, include_words=args.include_words, page_options=page_options
        )
    try:
        include_words = args.include_words
    except AttributeError:
        include_words = False
    display_doc(args.output_type, include_words, parsed_data)


def process_parse_queued(args: Namespace, client: Client, doc_class) -> None:
    """Processes the results of a queued parsing request."""
    input_doc = client.doc_for_async()
    if args.product_name == "custom":
        parsed_data = input_doc.parse_queued(
            document_class=doc_class,
            queue_id=args.queue_id,
            endpoint_name=args.endpoint_name,
            account_name=args.account_name,
        )
    else:
        parsed_data = input_doc.parse_queued(
            document_class=doc_class, queue_id=args.queue_id
        )
    if parsed_data.job.status == "completed" and parsed_data.document is not None:
        try:
            include_words = args.include_words
        except AttributeError:
            include_words = False
        display_doc(args.output_type, include_words, parsed_data.document)
    else:
        print(parsed_data.job)


def display_doc(output_type: str, include_words: bool, response: PredictResponse):
    """Display the parsed document."""
    if output_type == "raw":
        print(json.dumps(response.http_response, indent=2))
    elif output_type == "parsed":
        if include_words:
            print(json.dumps(response.ocr, indent=2, default=serialize_for_json))
        print(json.dumps(response.document, indent=2, default=serialize_for_json))
    else:
        if include_words:
            print("OCR Begin >>>>>>>>>>\n")
            print(response.ocr)
            print("<<<<<<<<<< OCR End\n")
        print(response.document)


def process_parse_enqueue(args: Namespace, client: Client, doc_class) -> None:
    """Processes the results of an enqueuing request."""
    if args.cut_doc and args.doc_pages:
        page_options = PageOptions(range(args.doc_pages), on_min_pages=0)
    else:
        page_options = None
    input_doc = _get_input_doc(client, args)
    if args.product_name == "custom":
        client.add_endpoint(
            endpoint_name=args.endpoint_name,
            account_name=args.account_name,
            version=args.api_version,
        )
        parsed_data = input_doc.enqueue(
            doc_class,
            endpoint_name=args.endpoint_name,
            account_name=args.account_name,
            page_options=page_options,
        )
    else:
        parsed_data = input_doc.enqueue(
            doc_class, include_words=args.include_words, page_options=page_options
        )
    print(parsed_data.job)


def _parse_args() -> Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Mindee API")
    parser.add_argument(
        "-E",
        "--no-raise-errors",
        action="store_false",
        dest="raise_on_error",
        help="don't raise errors",
    )
    subparsers = parser.add_subparsers(
        dest="product_name",
        required=True,
    )

    for name, info in DOCUMENTS.items():
        subp = subparsers.add_parser(name, help=info.help)
        parsers_call_method = subp.add_subparsers(dest="call_method", required=True)

        if info.is_sync:
            parser_predict = parsers_call_method.add_parser(
                "parse", help=f"Parse {name}"
            )
            _add_main_options(parser_predict)
            _add_sending_options(parser_predict)
            _add_display_options(parser_predict)
            if name == "custom":
                _add_custom_options(parser_predict)
            else:
                parser_predict.add_argument(
                    "-t",
                    "--full-text",
                    dest="include_words",
                    action="store_true",
                    help="include full document text in response",
                )

        if info.is_async:
            parser_enqueue = parsers_call_method.add_parser(
                "enqueue", help=f"Enqueue {name}"
            )
            _add_main_options(parser_enqueue)
            _add_sending_options(parser_enqueue)
            if name == "custom":
                _add_custom_options(parser_enqueue)
            else:
                parser_enqueue.add_argument(
                    "-t",
                    "--full-text",
                    dest="include_words",
                    action="store_true",
                    help="include full document text in response",
                )

            parser_parse_queued = parsers_call_method.add_parser(
                "parse-queued", help=f"Parse (queued) {name}"
            )
            _add_main_options(parser_parse_queued)
            _add_display_options(parser_parse_queued)
            parser_parse_queued.add_argument(
                dest="queue_id", help="Async queue ID for a document (required)"
            )

    parsed_args = parser.parse_args()
    return parsed_args


def _add_main_options(parser: ArgumentParser):
    parser.add_argument(
        "-k",
        "--key",
        dest="api_key",
        help="API key for the account",
    )


def _add_display_options(parser: ArgumentParser):
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


def _add_sending_options(parser: ArgumentParser):
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


def _add_custom_options(parser: ArgumentParser):
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


def main() -> None:
    """Run the Command Line Interface."""
    call_endpoint(_parse_args())
