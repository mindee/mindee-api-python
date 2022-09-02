import json

import pytest

from mindee import Client
from mindee.documents.base import Document
from mindee.documents.financial_document import FinancialDocument
from mindee.documents.invoice import Invoice
from mindee.documents.receipt import Receipt
from mindee.inputs import PathDocument
from mindee.response import format_response
from tests.documents.test_invoice import INVOICE_FILE_PATH
from tests.documents.test_receipt import RECEIPT_FILE_PATH


@pytest.fixture
def dummy_file_input():
    file_input = PathDocument("./tests/data/receipt/receipt.jpg")
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
    parsed_response = format_response(
        dummy_config[("mindee", "invoice")],
        response,
        dummy_file_input,
    )
    assert isinstance(parsed_response.document, Invoice)
    for page in parsed_response.pages:
        assert isinstance(page, Invoice)
    assert isinstance(parsed_response.invoice, Invoice)
    for page in parsed_response.invoices:
        assert isinstance(page, Invoice)


# Receipt tests


def test_response_wrapper_receipt(dummy_file_input, dummy_config):
    response = json.load(open(RECEIPT_FILE_PATH))
    parsed_response = format_response(
        dummy_config[("mindee", "receipt")], response, dummy_file_input
    )
    assert isinstance(parsed_response.document, Receipt)
    for page in parsed_response.pages:
        assert isinstance(page, Receipt)
    assert isinstance(parsed_response.receipt, Receipt)
    for page in parsed_response.receipts:
        assert isinstance(page, Receipt)


# Financial document tests


def test_response_wrapper_financial_doc_with_receipt(dummy_file_input, dummy_config):
    response = json.load(open(RECEIPT_FILE_PATH))
    parsed_response = format_response(
        dummy_config[("mindee", "financial_doc")],
        response,
        dummy_file_input,
    )
    assert isinstance(parsed_response.document, FinancialDocument)
    for page in parsed_response.pages:
        assert isinstance(page, FinancialDocument)
    assert isinstance(parsed_response.financial_doc, FinancialDocument)
    for page in parsed_response.financial_docs:
        assert isinstance(page, FinancialDocument)
