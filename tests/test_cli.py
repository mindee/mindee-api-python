from argparse import Namespace

import pytest

from mindee.cli import MindeeParser
from mindee.mindee_http.error import HTTPException
from tests.utils import clear_envvars


@pytest.fixture
def custom_doc(monkeypatch):
    clear_envvars(monkeypatch)
    return Namespace(
        product_name="custom",
        endpoint_name="license_plate",
        account_name="mindee",
        api_key="dummy",
        api_version="1",
        cut_doc=False,
        doc_pages=3,
        input_type="path",
        output_type="summary",
        include_words=False,
        path="./tests/data/file_types/pdf/blank.pdf",
        # parse_type="parse",
        async_parse=False,
    )


@pytest.fixture
def ots_doc(monkeypatch):
    clear_envvars(monkeypatch)
    return Namespace(
        api_key="dummy",
        cut_doc=False,
        doc_pages=3,
        input_type="path",
        output_type="summary",
        include_words=False,
        path="./tests/data/products/invoices/invoice.pdf",
        # parse_type="parse",
        async_parse=False,
    )


@pytest.fixture
def ots_doc_enqueue_and_parse(monkeypatch):
    clear_envvars(monkeypatch)
    return Namespace(
        api_key="dummy",
        cut_doc=False,
        doc_pages=3,
        input_type="path",
        include_words=False,
        path="./tests/data/products/invoice_splitter/default_sample.pdf",
        # parse_type="parse",
        async_parse=True,
    )


@pytest.fixture
def ots_doc_fetch(monkeypatch):
    clear_envvars(monkeypatch)
    return Namespace(
        api_key="dummy",
        output_type="summary",
        queue_id="dummy-queue-id",
        call_method="parse-queued",
        # parse_type="fetch",
    )


def test_cli_custom_doc(custom_doc):
    with pytest.raises(HTTPException):
        parser = MindeeParser(parsed_args=custom_doc)
        parser.call_endpoint()


def test_cli_invoice(ots_doc):
    ots_doc.product_name = "invoice"
    ots_doc.api_key = ""
    with pytest.raises(RuntimeError):
        parser = MindeeParser(parsed_args=ots_doc)
        parser.call_endpoint()
    ots_doc.api_key = "dummy"
    with pytest.raises(HTTPException):
        parser = MindeeParser(parsed_args=ots_doc)
        parser.call_endpoint()


def test_cli_receipt(ots_doc):
    ots_doc.product_name = "receipt"
    ots_doc.api_key = ""
    with pytest.raises(RuntimeError):
        parser = MindeeParser(parsed_args=ots_doc)
        parser.call_endpoint()
    ots_doc.api_key = "dummy"
    with pytest.raises(HTTPException):
        parser = MindeeParser(parsed_args=ots_doc)
        parser.call_endpoint()


def test_cli_financial_doc(ots_doc):
    ots_doc.product_name = "financial-document"
    ots_doc.api_key = ""
    with pytest.raises(RuntimeError):
        parser = MindeeParser(parsed_args=ots_doc)
        parser.call_endpoint()
    ots_doc.api_key = "dummy"
    with pytest.raises(HTTPException):
        parser = MindeeParser(parsed_args=ots_doc)
        parser.call_endpoint()


def test_cli_passport(ots_doc):
    ots_doc.product_name = "passport"
    ots_doc.api_key = ""
    with pytest.raises(RuntimeError):
        parser = MindeeParser(parsed_args=ots_doc)
        parser.call_endpoint()
    ots_doc.api_key = "dummy"
    with pytest.raises(HTTPException):
        parser = MindeeParser(parsed_args=ots_doc)
        parser.call_endpoint()


def test_cli_us_bank_check(ots_doc):
    ots_doc.product_name = "us-bank-check"
    ots_doc.api_key = ""
    with pytest.raises(RuntimeError):
        parser = MindeeParser(parsed_args=ots_doc)
        parser.call_endpoint()
    ots_doc.api_key = "dummy"
    with pytest.raises(HTTPException):
        parser = MindeeParser(parsed_args=ots_doc)
        parser.call_endpoint()


def test_cli_invoice_splitter_enqueue(ots_doc_enqueue_and_parse):
    ots_doc_enqueue_and_parse.product_name = "invoice-splitter"
    ots_doc_enqueue_and_parse.api_key = ""
    with pytest.raises(RuntimeError):
        parser = MindeeParser(parsed_args=ots_doc_enqueue_and_parse)
        parser.call_endpoint()
    ots_doc_enqueue_and_parse.api_key = "dummy"
    with pytest.raises(HTTPException):
        parser = MindeeParser(parsed_args=ots_doc_enqueue_and_parse)
        parser.call_endpoint()


# def test_cli_invoice_splitter_parse_queued(ots_doc_fetch):
#     ots_doc_fetch.product_name = "invoice-splitter"
#     ots_doc_fetch.api_key = ""
#     with pytest.raises(RuntimeError):
#         parser = MindeeParser(parsed_args=ots_doc_fetch)
#         parser.call_endpoint()
#     ots_doc_fetch.api_key = "dummy"
#     with pytest.raises(HTTPException):
#         parser = MindeeParser(parsed_args=ots_doc_fetch)
#         parser.call_endpoint()
