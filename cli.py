#! /usr/bin/env python3

import argparse
import os
import sys

from mindee import Client

PRODUCTS = {
    "invoice": {
        "help": "invoices api",
        "token_name": "invoice_api_key",
        "doc_type": "invoice",
    },
    "receipt": {
        "help": "expense receipt api",
        "token_name": "receipt_api_key",
        "doc_type": "receipt",
    },
    "passport": {
        "help": "passport api",
        "token_name": "passport_token",
        "doc_type": "passport",
    },
}


def get_env_token(name: str) -> str:
    return os.getenv(f"MINDEE_{name.upper()}_TOKEN", "")


def call_endpoint(args):
    product_info = PRODUCTS[args.product_name]
    kwargs = {
        product_info["token_name"]: args.token,
        "raise_on_error": args.raise_on_error,
    }
    client = Client(**kwargs)
    if args.input_type == "stream":
        with open(args.path, "rb", buffering=30) as file_handle:
            parsed_data = client.parse_from_file(
                file_handle, product_info["doc_type"], cut_pdf=args.cut_pdf
            )
    elif args.input_type == "base64":
        with open(args.path, "rt") as file_handle:
            parsed_data = client.parse_from_b64string(
                file_handle.read(),
                "test.jpg",
                product_info["doc_type"],
                cut_pdf=args.cut_pdf,
            )
    else:
        parsed_data = client.parse_from_path(
            args.path, product_info["doc_type"], cut_pdf=args.cut_pdf
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
    for name, info in PRODUCTS.items():
        subp = subparsers.add_parser(name, help=info["help"])
        subp.add_argument(
            "-t",
            "--token",
            dest="token",
            default=get_env_token(name),
            help="Token for product",
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
