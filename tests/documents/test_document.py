import json

import pytest

from mindee import Client
from mindee.documents.base import Document
from mindee.inputs import PathDocument
from mindee.response import format_response
from tests.documents.test_invoice import INVOICE_FILE_PATH
from tests.documents.test_receipt import RECEIPT_FILE_PATH


@pytest.fixture
def dummy_file_input():
    file_input = PathDocument("./tests/data/expense_receipts/receipt.jpg")
    return file_input


@pytest.fixture
def dummy_config():
    client = (
        Client()
        .config_receipt("dummy")
        .config_invoice("dummy")
        .config_passport("dummy")
        .config_financial_doc("dummy", "dummy")
        .config_custom_doc(
            document_type="dummy",
            singular_name="dummy",
            plural_name="dummies",
            account_name="dummy",
        )
    )
    return client._doc_configs


def test_constructor(dummy_file_input):
    with pytest.raises(NotImplementedError):
        Document(dummy_file_input, document_type="receipt", api_prediction={}, page_n=0)


# Invoice tests


def test_response_wrapper_invoice(dummy_file_input, dummy_config):
    response = json.load(open(INVOICE_FILE_PATH))
    parsed_invoice = format_response(
        dummy_config[("mindee", "invoice")],
        response,
        "invoice",
        dummy_file_input,
    )
    assert parsed_invoice.invoice.invoice_date.value == "2020-02-17"


# Receipt tests


def test_response_wrapper_receipt(dummy_file_input, dummy_config):
    response = json.load(open(RECEIPT_FILE_PATH))
    parsed_receipt = format_response(
        dummy_config[("mindee", "receipt")], response, "receipt", dummy_file_input
    )
    assert parsed_receipt.receipt.date.value == "2016-02-26"


# Financial document tests


def test_response_wrapper_financial_doc_with_receipt(dummy_file_input, dummy_config):
    response = json.load(open(RECEIPT_FILE_PATH))
    parsed_financial_doc = format_response(
        dummy_config[("mindee", "financial_doc")],
        response,
        "financial",
        dummy_file_input,
    )
    assert parsed_financial_doc.financial_doc.date.value == "2016-02-26"


def test_response_wrapper_financial_doc_with_invoice(dummy_file_input, dummy_config):
    response = json.load(open(INVOICE_FILE_PATH))
    parsed_financial_doc = format_response(
        dummy_config[("mindee", "financial_doc")],
        response,
        "financial",
        dummy_file_input,
    )
    assert parsed_financial_doc.financial_doc.date.value == "2020-02-17"
