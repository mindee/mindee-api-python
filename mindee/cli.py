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
    "shipping-container": CommandConfig(
        help="Shipping Container",
        doc_class=documents.fr.TypeIdCardV1,
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

    if args.instruction_type == "enqueue":
        process_parse_enqueue(args, client, doc_class)
    elif args.instruction_type == "parse-queued":
        process_parse_queued(args, client, doc_class)
    elif args.instruction_type == "parse":
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
            endpoint_name=args.api_name,
            account_name=args.username,
            version=args.api_version,
        )
        parsed_data = input_doc.parse(
            doc_class,
            endpoint_name=args.api_name,
            account_name=args.username,
            page_options=page_options,
        )
    else:
        parsed_data = input_doc.parse(
            doc_class, include_words=args.include_words, page_options=page_options
        )
    display_doc(args.output_type, parsed_data)


def process_parse_queued(args: Namespace, client: Client, doc_class) -> None:
    """Processes the results of a queued parsing request."""
    input_doc = client.doc_for_async()
    if args.product_name == "custom":
        parsed_data = input_doc.parse_queued(
            document_class=doc_class,
            queue_id=args.queue_id,
            endpoint_name=args.api_name,
            account_name=args.username,
        )
    else:
        parsed_data = input_doc.parse_queued(
            document_class=doc_class, queue_id=args.queue_id
        )
    if parsed_data.job.status == "completed" and parsed_data.document is not None:
        display_doc(args.output_type, parsed_data.document)
    else:
        print(parsed_data.job)


def display_doc(output_type: str, document_response: PredictResponse):
    """Display the parsed document."""
    if output_type == "raw":
        print(json.dumps(document_response.http_response, indent=2))
    elif output_type == "parsed":
        doc = document_response.document
        print(json.dumps(doc, indent=2, default=serialize_for_json))
    else:
        print(document_response.document)


def process_parse_enqueue(args: Namespace, client: Client, doc_class) -> None:
    """Processes the results of an enqueuing request."""
    if args.cut_doc and args.doc_pages:
        page_options = PageOptions(range(args.doc_pages), on_min_pages=0)
    else:
        page_options = None
    input_doc = _get_input_doc(client, args)
    if args.product_name == "custom":
        client.add_endpoint(
            endpoint_name=args.api_name,
            account_name=args.username,
            version=args.api_version,
        )
        parsed_data = input_doc.enqueue(
            doc_class,
            endpoint_name=args.api_name,
            account_name=args.username,
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
        parsers_instruction_type = subp.add_subparsers(
            dest="instruction_type", required=True
        )

        if info.is_sync:
            subp_predict = parsers_instruction_type.add_parser(
                "parse", help=f"Parse {name}"
            )
            _add_options(subp_predict, "predict", name)
            subp_predict.add_argument(dest="path", help="Full path to the file")

        if info.is_async:
            parser_enqueue = parsers_instruction_type.add_parser(
                "enqueue", help=f"Enqueue {name}"
            )
            _add_options(parser_enqueue, "enqueue", name)
            parser_enqueue.add_argument(dest="path", help="Full path to the file")

            parser_parse_queued = parsers_instruction_type.add_parser(
                "parse-queued", help=f"Parse (queued) {name}"
            )
            _add_options(parser_parse_queued, "parse-queued", name)
            parser_parse_queued.add_argument(
                dest="queue_id", help="Async queue ID for a document (required)"
            )

    parsed_args = parser.parse_args()
    return parsed_args


def _add_options(parser: ArgumentParser, category: str, name: str):
    """Adds options to a given command."""
    parser.add_argument(
        "-k",
        "--key",
        dest="api_key",
        help="API key for the account",
    )

    if category in ["predict", "enqueue"]:
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

        if name == "custom":
            parser.add_argument(
                "-a",
                "--account-name",
                dest="username",
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
        else:
            parser.add_argument(
                "-t",
                "--full-text",
                dest="include_words",
                action="store_true",
                help="include full document text in response",
            )

    if category in ["predict", "parse-queued"]:
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


def main() -> None:
    """Run the Command Line Interface."""
    call_endpoint(_parse_args())
