#! /usr/bin/env python3

import argparse
import os
import sys
from typing import Dict

from mindee import Client

DOCUMENTS: Dict[str, dict] = {
    "invoice": {
        "help": "Invoice",
        "required_keys": ["invoice"],
        "parse_func": "parse_invoice",
        "doc_type": "invoice",
    },
    "receipt": {
        "help": "Expense Receipt",
        "required_keys": ["expense_receipt"],
        "parse_func": "parse_receipt",
        "doc_type": "receipt",
    },
    "passport": {
        "help": "Passport",
        "required_keys": ["passport"],
        "parse_func": "parse_passport",
        "doc_type": "passport",
    },
    "financial": {
        "help": "Financial Document (receipt or invoice)",
        "required_keys": ["invoice", "expense_receipt"],
        "parse_func": "parse_financial_document",
        "doc_type": "financial_document",
    },
}


def _get_env_token(name: str) -> str:
    return os.getenv(f"MINDEE_{name.upper()}_TOKEN", "")


def call_endpoint(args):
    """Call the endpoint given passed arguments."""
    info = DOCUMENTS[args.product_name]
    kwargs = {
        "raise_on_error": args.raise_on_error,
    }
    for key in info["required_keys"]:
        kwargs["%s_token" % key] = getattr(args, "%s_api_key" % key)
    client = Client(**kwargs)
    parse_func = getattr(client, info["parse_func"])
    if args.input_type == "stream":
        with open(args.path, "rb", buffering=30) as file_handle:
            parsed_data = parse_func(file_handle, args.input_type, cut_pdf=args.cut_pdf)
    elif args.input_type == "base64":
        with open(args.path, "rt") as file_handle:
            parsed_data = parse_func(
                file_handle.read(),
                args.input_type,
                filename=args.filename,
                cut_pdf=args.cut_pdf,
            )
    else:
        parsed_data = parse_func(args.path, args.input_type, cut_pdf=args.cut_pdf)
    print(getattr(parsed_data, info["doc_type"]))


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Mindee API")
    parser.add_argument(
        "-e",
        "--no-raise-errors",
        action="store_false",
        dest="raise_on_error",
        help="don't raise errors",
    )
    subparsers = parser.add_subparsers(
        dest="product_name",
        help="sub-command help",
    )
    for name, info in DOCUMENTS.items():
        subp = subparsers.add_parser(name, help=info["help"])
        for key_name in info["required_keys"]:
            subp.add_argument(
                "--%s-key" % key_name,
                dest="%s_api_key" % key_name,
                help="API key for %s document endpoint" % key_name,
                default=_get_env_token(key_name),
            )
        subp.add_argument(
            "-i",
            "--input-type",
            dest="input_type",
            choices=["path", "stream", "base64"],
            default="path",
            help="Specify how to handle the input,\n"
            "path: open the file.\n"
            "stream: open the file in a buffer.\n"
            "base64: load the contents as a string.",
        )
        subp.add_argument(
            "-f",
            "--filename",
            dest="filename",
            help="filename (required for base64 inputs)",
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
