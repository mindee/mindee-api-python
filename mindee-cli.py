#! /usr/bin/env python3

import argparse
import os
import sys

from mindee import Client

DOCUMENTS = {
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
    "financial-document": {
        "help": "Financial Document",
        "required_keys": ["invoice", "receipt"],
        "doc_type": "financial_document",
    },
}


def call_endpoint(args):
    info = DOCUMENTS[args.product_name]
    kwargs = {
        "raise_on_error": args.raise_on_error,
    }
    for key in info["required_keys"]:
        kwargs["%s_api_key" % key] = getattr(args, "%s_api_key" % key)
    client = Client(**kwargs)
    if args.input_type == "stream":
        with open(args.path, "rb", buffering=30) as file_handle:
            parsed_data = client.parse_from_file(
                file_handle, info["doc_type"], cut_pdf=args.cut_pdf
            )
    elif args.input_type == "base64":
        with open(args.path, "rt") as file_handle:
            parsed_data = client.parse_from_b64string(
                file_handle.read(),
                "test.jpg",
                info["doc_type"],
                cut_pdf=args.cut_pdf,
            )
    else:
        parsed_data = client.parse_from_path(
            args.path, info["doc_type"], cut_pdf=args.cut_pdf
        )
    print(getattr(parsed_data, args.product_name))


def parse_args():
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
            )
        subp.add_argument(
            "-t",
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
