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
        api_name="license_plate",
        username="mindee",
        api_key="dummy",
        api_version="1",
        raise_on_error=True,
        cut_doc=False,
        doc_pages=3,
        input_type="path",
        output_type="summary",
        include_words=False,
        path="./tests/data/pdf/blank.pdf",
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
        path="./tests/data/invoice/invoice.pdf",
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
