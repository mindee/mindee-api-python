from argparse import Namespace

import pytest

from mindee.cli import call_endpoint
from mindee.endpoints import HTTPException
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
        raise_on_error=True,
        cut_doc=False,
        doc_pages=3,
        input_type="path",
        output_type="summary",
        include_words=False,
        path="./tests/data/file_types/pdf/blank.pdf",
        call_method="parse",
    )


@pytest.fixture
def ots_doc(monkeypatch):
    clear_envvars(monkeypatch)
    return Namespace(
        api_key="dummy",
        raise_on_error=True,
        cut_doc=False,
        doc_pages=3,
        input_type="path",
        output_type="summary",
        include_words=False,
        path="./tests/data/products/invoices/invoice.pdf",
        call_method="parse",
    )


@pytest.fixture
def ots_doc_enqueue(monkeypatch):
    clear_envvars(monkeypatch)
    return Namespace(
        api_key="dummy",
        raise_on_error=True,
        cut_doc=False,
        doc_pages=3,
        input_type="path",
        include_words=False,
        path="./tests/data/products/invoice_splitter/default_sample.pdf",
        call_method="enqueue",
    )


@pytest.fixture
def ots_doc_parse_queued(monkeypatch):
    clear_envvars(monkeypatch)
    return Namespace(
        api_key="dummy",
        raise_on_error=True,
        output_type="summary",
        queue_id="dummy-queue-id",
        call_method="parse-queued",
    )


def test_cli_custom_doc(custom_doc):
    with pytest.raises(HTTPException):
        call_endpoint(custom_doc)


def test_cli_invoice(ots_doc):
    ots_doc.product_name = "invoice"
    ots_doc.api_key = ""
    with pytest.raises(RuntimeError):
        call_endpoint(ots_doc)
    ots_doc.api_key = "dummy"
    with pytest.raises(HTTPException):
        call_endpoint(ots_doc)


def test_cli_receipt(ots_doc):
    ots_doc.product_name = "receipt"
    ots_doc.api_key = ""
    with pytest.raises(RuntimeError):
        call_endpoint(ots_doc)
    ots_doc.api_key = "dummy"
    with pytest.raises(HTTPException):
        call_endpoint(ots_doc)


def test_cli_financial_doc(ots_doc):
    ots_doc.product_name = "financial-document"
    ots_doc.api_key = ""
    with pytest.raises(RuntimeError):
        call_endpoint(ots_doc)
    ots_doc.api_key = "dummy"
    with pytest.raises(HTTPException):
        call_endpoint(ots_doc)


def test_cli_passport(ots_doc):
    ots_doc.product_name = "passport"
    ots_doc.api_key = ""
    with pytest.raises(RuntimeError):
        call_endpoint(ots_doc)
    ots_doc.api_key = "dummy"
    with pytest.raises(HTTPException):
        call_endpoint(ots_doc)


def test_cli_us_bank_check(ots_doc):
    ots_doc.product_name = "us-bank-check"
    ots_doc.api_key = ""
    with pytest.raises(RuntimeError):
        call_endpoint(ots_doc)
    ots_doc.api_key = "dummy"
    with pytest.raises(HTTPException):
        call_endpoint(ots_doc)


def test_cli_invoice_splitter_enqueue(ots_doc_enqueue):
    ots_doc_enqueue.product_name = "invoice-splitter"
    ots_doc_enqueue.api_key = ""
    with pytest.raises(RuntimeError):
        call_endpoint(ots_doc_enqueue)
    ots_doc_enqueue.api_key = "dummy"
    with pytest.raises(HTTPException):
        call_endpoint(ots_doc_enqueue)


def test_cli_invoice_splitter_parse_queued(ots_doc_parse_queued):
    ots_doc_parse_queued.product_name = "invoice-splitter"
    ots_doc_parse_queued.api_key = ""
    with pytest.raises(RuntimeError):
        call_endpoint(ots_doc_parse_queued)
    ots_doc_parse_queued.api_key = "dummy"
    with pytest.raises(HTTPException):
        call_endpoint(ots_doc_parse_queued)
