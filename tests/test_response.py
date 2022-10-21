import json

import pytest

from mindee import Client
from mindee.documents.base import Document
from mindee.documents.financial_document import FinancialDocument
from mindee.documents.invoice import Invoice
from mindee.documents.passport import Passport
from mindee.documents.receipt import Receipt
from mindee.input.sources import PathInput
from mindee.response import PredictResponse
from tests.documents.test_invoice import INVOICE_FILE_PATH
from tests.documents.test_passport import PASSPORT_FILE_PATH
from tests.documents.test_receipt import RECEIPT_FILE_PATH


@pytest.fixture
def dummy_file_input():
    file_input = PathInput("./tests/data/receipt/receipt.jpg")
    return file_input


@pytest.fixture
def dummy_config():
    client = Client(api_key="dummy").add_endpoint(
        endpoint_name="dummy",
        account_name="dummy",
    )
    return client._doc_configs


def test_constructor(dummy_file_input):
    with pytest.raises(NotImplementedError):
        Document(dummy_file_input, document_type="receipt", api_prediction={}, page_n=0)


def test_response_invoice(dummy_file_input, dummy_config):
    response = json.load(open(INVOICE_FILE_PATH))
    parsed_response = PredictResponse[Invoice](
        doc_config=dummy_config[("mindee", "invoice")],
        http_response=response,
        input_source=dummy_file_input,
        response_ok=True,
    )
    assert isinstance(parsed_response.document, Invoice)
    for page in parsed_response.pages:
        assert isinstance(page, Invoice)


def test_response_receipt(dummy_file_input, dummy_config):
    response = json.load(open(RECEIPT_FILE_PATH))
    parsed_response = PredictResponse[Receipt](
        doc_config=dummy_config[("mindee", "receipt")],
        http_response=response,
        input_source=dummy_file_input,
        response_ok=True,
    )
    assert isinstance(parsed_response.document, Receipt)
    for page in parsed_response.pages:
        assert isinstance(page, Receipt)


def test_response_financial_doc_with_receipt(dummy_file_input, dummy_config):
    response = json.load(open(RECEIPT_FILE_PATH))
    parsed_response = PredictResponse[FinancialDocument](
        doc_config=dummy_config[("mindee", "financial_doc")],
        http_response=response,
        input_source=dummy_file_input,
        response_ok=True,
    )
    assert isinstance(parsed_response.document, FinancialDocument)
    for page in parsed_response.pages:
        assert isinstance(page, FinancialDocument)


def test_response_passport(dummy_file_input, dummy_config):
    response = json.load(open(PASSPORT_FILE_PATH))
    parsed_response = PredictResponse[Passport](
        doc_config=dummy_config[("mindee", "passport")],
        http_response=response,
        input_source=dummy_file_input,
        response_ok=True,
    )
    assert isinstance(parsed_response.document, Passport)
    for page in parsed_response.pages:
        assert isinstance(page, Passport)
