import pytest
import json
from mindee import Response, Client
from mindee.inputs import Inputs
from mindee.documents.base import Document


@pytest.fixture
def dummy_file_input():
    file_input = Inputs("./tests/data/expense_receipts/receipt.jpg")
    return file_input


@pytest.fixture
def dummy_client():
    return Client(
        receipt_api_key="dummy",
        invoice_api_key="dummy",
        passport_api_key="dummy",
    )


def test_constructor():
    document = Document()
    assert document.checklist == {}
    with pytest.raises(NotImplementedError):
        document.request([], "")
    with pytest.raises(NotImplementedError):
        document._checklist()


# Invoice tests


def test_response_wrapper_invoice(dummy_file_input, dummy_client):
    response = json.load(open("./tests/data/invoices/v2/invoice.json"))
    parsed_invoice = Response.format_response(
        dummy_client, response, "invoice", dummy_file_input
    )
    assert parsed_invoice.invoice.invoice_date.value == "2018-09-25"


# Receipt tests


def test_responseWrapper_receipt(dummy_file_input, dummy_client):
    response = json.load(open("./tests/data/expense_receipts/v3/receipt.json"))
    parsed_receipt = Response.format_response(
        dummy_client, response, "receipt", dummy_file_input
    )
    assert parsed_receipt.receipt.date.value == "2016-02-26"


# Financial document tests


def test_responseWrapper_financial_document_with_receipt(
    dummy_file_input, dummy_client
):
    response = json.load(open("./tests/data/expense_receipts/v3/receipt.json"))
    parsed_financial_doc = Response.format_response(
        dummy_client, response, "financial_document", dummy_file_input
    )
    assert parsed_financial_doc.financial_document.date.value == "2016-02-26"


def test_responseWrapper_financial_document_with_invoice(
    dummy_file_input, dummy_client
):
    response = json.load(open("./tests/data/invoices/v2/invoice.json"))
    parsed_financial_doc = Response.format_response(
        dummy_client, response, "financial_document", dummy_file_input
    )
    assert parsed_financial_doc.financial_document.date.value == "2018-09-25"
