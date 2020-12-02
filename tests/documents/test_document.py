import pytest
import json
from mindee import Response, Inputs
from mindee.documents import Document


@pytest.fixture
def dummy_file_input():
    file_input = Inputs("./tests/data/expense_receipts/receipt.jpg")
    return file_input


def test_constructor():
    document = Document()
    assert document.checklist == {}
    with pytest.raises(NotImplementedError):
        document.request()
    with pytest.raises(NotImplementedError):
        document._checklist()


# Plate tests

def test_responseWrapper_plate(dummy_file_input):
    response = json.load(open('./tests/data/license_plates/v1/plate.json'))
    parsed_plate = Response.format_response(response, "license_plate", dummy_file_input)
    assert parsed_plate.license_plate.license_plates[0].value == "7EQE707"


# Invoice tests

def test_responseWrapper_invoice(dummy_file_input):
    response = json.load(open('./tests/data/invoices/v2/invoice.json'))
    parsed_invoice = Response.format_response(response, "invoice", dummy_file_input)
    assert parsed_invoice.invoice.invoice_date.value == "2020-02-17"


from mindee import Invoice

json_repsonse = json.load(open("./tests/data/invoices/v2/invoice.json"))
invoice_0 = Invoice(json_repsonse["predictions"][0])
invoice_1 = Invoice(json_repsonse["predictions"][1])


def test_merge_pages():
    merge_document = Document.merge_pages([invoice_0, invoice_1])
    assert merge_document.invoice_date.value == "2020-02-17"


# Receipt tests

def test_responseWrapper_receipt(dummy_file_input):
    response = json.load(open('./tests/data/expense_receipts/v3/receipt.json'))
    parsed_receipt = Response.format_response(response, "receipt", dummy_file_input)
    assert parsed_receipt.receipt.date.value == "2016-02-26"


# Financial document tests

def test_responseWrapper_financial_document_with_receipt(dummy_file_input):
    response = json.load(open('./tests/data/expense_receipts/v3/receipt.json'))
    parsed_financial_doc = Response.format_response(response, "financial_document", dummy_file_input)
    assert parsed_financial_doc.financial_document.date.value == "2016-02-26"


def test_responseWrapper_financial_document_with_invoice(dummy_file_input):
    response = json.load(open('./tests/data/invoices/v2/invoice.json'))
    parsed_financial_doc = Response.format_response(response, "financial_document", dummy_file_input)
    assert parsed_financial_doc.financial_document.date.value == "2020-02-17"

