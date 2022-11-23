import argparse
import json
from argparse import Namespace
from dataclasses import dataclass
from typing import Dict, Generic, TypeVar

from mindee import Client, PageOptions, documents
from mindee.client import DocumentClient
from mindee.documents.base import Document, serialize_for_json

TypeDoc = TypeVar("TypeDoc", bound=Document)


@dataclass
class CommandConfig(Generic[TypeDoc]):
    help: str
    doc_class: TypeDoc


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
        doc_class=documents.TypeReceiptV4,
    ),
    "passport": CommandConfig(
        help="Passport",
        doc_class=documents.TypePassportV1,
    ),
    "financial": CommandConfig(
        help="Financial Document (receipt or invoice)",
        doc_class=documents.TypeFinancialV1,
    ),
    "us-check": CommandConfig(
        help="US Bank Check",
        doc_class=documents.us.TypeBankCheckV1,
    ),
}


def _get_input_doc(client, args) -> DocumentClient:
    if args.input_type == "file":
        with open(args.path, "rb", buffering=30) as file_handle:
            return client.doc_from_file(file_handle)
    elif args.input_type == "base64":
        with open(args.path, "rt", encoding="ascii") as base64_handle:
            return client.doc_from_b64string(base64_handle.read(), "test.jpg")
    elif args.input_type == "bytes":
        with open(args.path, "rb") as bytes_handle:
            return client.doc_from_bytes(bytes_handle.read(), bytes_handle.name)
    return client.doc_from_path(args.path)


def call_endpoint(args: Namespace):
    """Call the endpoint given passed arguments."""
    client = Client(api_key=args.api_key, raise_on_error=args.raise_on_error)
    if args.product_name == "custom":
        client.add_endpoint(
            endpoint_name=args.doc_type,
            account_name=args.username,
        )
    info = DOCUMENTS[args.product_name]
    doc_class = info.doc_class

    input_doc = _get_input_doc(client, args)

    if args.cut_doc and args.doc_pages:
        page_options = PageOptions(range(args.doc_pages), on_min_pages=0)
    else:
        page_options = None
    if args.product_name == "custom":
        parsed_data = input_doc.parse(
            doc_class,
            endpoint_name=args.doc_type,
            account_name=args.username,
            page_options=page_options,
        )
    else:
        parsed_data = input_doc.parse(
            doc_class, include_words=args.include_words, page_options=page_options
        )

    if args.output_type == "raw":
        print(json.dumps(parsed_data.http_response, indent=2))
    elif args.output_type == "parsed":
        doc = parsed_data.document
        print(json.dumps(doc, indent=2, default=serialize_for_json))
    else:
        print(parsed_data.document)


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
        if name == "custom":
            subp.add_argument(
                "-u",
                "--user",
                dest="username",
                required=True,
                help="API account name for the endpoint",
            )
            subp.add_argument(
                "-k",
                "--key",
                dest="api_key",
                help="API key for the endpoint",
            )
            subp.add_argument(dest="doc_type", help="Document type")
        else:
            subp.add_argument(
                "-k",
                "--key",
                dest="api_key",
                help="API key for the endpoint",
            )
            subp.add_argument(
                "-w",
                "--with-words",
                dest="include_words",
                action="store_true",
                help="Include words in response",
            )
        subp.add_argument(
            "-i",
            "--input-type",
            dest="input_type",
            choices=["path", "file", "base64", "bytes"],
            default="path",
            help="Specify how to handle the input.\n"
            "- path: open a path (default).\n"
            "- file: open as a file handle.\n"
            "- base64: load the from a base64 encoded text file.\n"
            "- bytes: load the contents as raw bytes.",
        )
        subp.add_argument(
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
        subp.add_argument(
            "-c",
            "--cut",
            dest="cut_doc",
            action="store_true",
            help="Cut document pages",
        )
        subp.add_argument(
            "-p",
            "--pages-keep",
            dest="doc_pages",
            type=int,
            default=5,
            help="Number of document pages to keep, default: 5",
        )
        subp.add_argument(dest="path", help="Full path to the file")

    parsed_args = parser.parse_args()
    return parsed_args


def main() -> None:
    """Run the Command Line Interface."""
    call_endpoint(_parse_args())


if __name__ == "__main__":
    main()
