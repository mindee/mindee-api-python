import argparse
from argparse import Namespace
import json
import sys
from typing import Dict

from mindee import Client

DOCUMENTS: Dict[str, dict] = {
    "invoice": {
        "help": "Invoice",
        "required_keys": ["invoice"],
        "doc_type": "invoice",
    },
    "receipt": {
        "help": "Expense Receipt",
        "required_keys": ["receipt"],
        "doc_type": "receipt",
    },
    "passport": {
        "help": "Passport",
        "required_keys": ["passport"],
        "doc_type": "passport",
    },
    "financial": {
        "help": "Financial Document (receipt or invoice)",
        "required_keys": ["invoice", "receipt"],
        "doc_type": "financial",
    },
    "custom": {
        "help": "Custom document type from API builder",
    },
}


def _ots_client(args: Namespace, info: dict):
    client = Client(raise_on_error=args.raise_on_error)
    kwargs = {}
    if len(info["required_keys"]) > 1:
        for key in info["required_keys"]:
            kwargs["%s_api_key" % key] = getattr(args, "%s_api_key" % key)
    else:
        kwargs["api_key"] = getattr(args, "%s_api_key" % args.product_name)
    func = getattr(client, f"config_{args.product_name}")
    func(**kwargs)
    return client


def _custom_client(args: Namespace):
    client = Client(raise_on_error=args.raise_on_error)
    client.config_custom_doc(
        document_type=args.doc_type,
        singular_name=args.doc_type,
        plural_name=args.doc_type + "s",
        account_name=args.username,
        api_key=args.api_key,
    )
    return client


def call_endpoint(args):
    """Call the endpoint given passed arguments."""
    if args.product_name == "custom":
        client = _custom_client(args)
        doc_type = args.doc_type
    else:
        info = DOCUMENTS[args.product_name]
        client = _ots_client(args, info)
        doc_type = info["doc_type"]

    if args.input_type == "file":
        with open(args.path, "rb", buffering=30) as file_handle:
            doc_to_parse = client.doc_from_file(file_handle, cut_pdf=args.cut_pdf)
    elif args.input_type == "base64":
        with open(args.path, "rt") as file_handle:
            doc_to_parse = client.doc_from_b64string(
                file_handle.read(), "test.jpg", cut_pdf=args.cut_pdf
            )
    elif args.input_type == "bytes":
        with open(args.path, "rb") as file_handle:
            doc_to_parse = client.doc_from_bytes(
                file_handle.read(), file_handle.name, cut_pdf=args.cut_pdf
            )
    else:
        doc_to_parse = client.doc_from_path(args.path, cut_pdf=args.cut_pdf)

    if args.product_name == "custom":
        parsed_data = doc_to_parse.parse(doc_type, username=args.username)
    else:
        parsed_data = doc_to_parse.parse(doc_type)

    if args.output_type == "raw":
        print(json.dumps(parsed_data.http_response, indent=2))
    elif args.output_type == "parsed":
        print(json.dumps(getattr(parsed_data, doc_type), indent=2, default=vars))
    else:
        print(getattr(parsed_data, doc_type))


def parse_args():
    """Parse command line arguments"""
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
        subp = subparsers.add_parser(name, help=info["help"])
        if name == "custom":
            subp.add_argument(
                "-u",
                "--user",
                dest="account_name",
                help="API account_name for the endpoint",
            )
            subp.add_argument(
                "-k",
                "--key",
                dest="api_key",
                help="API key for the endpoint",
            )
            subp.add_argument(dest="doc_type", help="Document type")
        else:
            for key_name in info["required_keys"]:
                subp.add_argument(
                    "--%s-key" % key_name,
                    dest="%s_api_key" % key_name,
                    help="API key for %s document endpoint" % key_name,
                )
        subp.add_argument(
            "-i",
            "--input-type",
            dest="input_type",
            choices=["path", "file", "base64", "bytes"],
            default="path",
            help="Specify how to handle the input,\n"
            "path: open a path (default).\n"
            "file: open as a file handle.\n"
            "base64: load the from a base64 encoded text file.\n"
            "bytes: load the contents as raw bytes.",
        )
        subp.add_argument(
            "-o",
            "--output-type",
            dest="output_type",
            choices=["summary", "raw", "parsed"],
            default="summary",
            help="Specify how to output the data,\n"
            "summary: a basic summary (default)\n"
            "raw: the raw HTTP response\n"
            "parsed: the validated and parsed data fields\n",
        )
        subp.add_argument(
            "-C",
            "--no-cut-pdf",
            dest="cut_pdf",
            action="store_false",
            help="Don't cut the PDF",
        )
        subp.add_argument(
            "-p",
            "--pdf-pages",
            dest="pdf_pages",
            type=int,
            default=3,
            help="Number of PDF pages to cut by, default: 3",
        )
        subp.add_argument(dest="path", help="Full path to the file")

    parsed_args = parser.parse_args()
    if not parsed_args.product_name:
        parser.print_help()
        sys.exit(1)
    return parsed_args


if __name__ == "__main__":
    call_endpoint(parse_args())
