import json

import pytest

from mindee import Client
from mindee.documents.base import Document
from mindee.documents.financial.financial_document_v1 import FinancialDocumentV1
from mindee.documents.invoice.invoice_v3 import InvoiceV3
from mindee.documents.passport.passport_v1 import PassportV1
from mindee.documents.receipt.receipt_v3 import ReceiptV3
from mindee.documents.receipt.receipt_v4 import ReceiptV4
from mindee.endpoints import OTS_OWNER
from mindee.input.sources import PathInput
from mindee.response import PredictResponse
from tests.documents.test_financial_document_v1 import (
    FILE_PATH_FINANCIAL_DOC_V1_RECEIPT,
)
from tests.documents.test_invoice_v3 import FILE_PATH_INVOICE_V3_COMPLETE
from tests.documents.test_passport_v1 import FILE_PATH_PASSPORT_V1_COMPLETE
from tests.documents.test_receipt_v3 import FILE_PATH_RECEIPT_V3_COMPLETE
from tests.documents.test_receipt_v4 import FILE_PATH_RECEIPT_V4_COMPLETE


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
    with pytest.raises(KeyError):
        Document(dummy_file_input, document_type="receipt", api_prediction={}, page_n=0)


def test_response_invoice_v3(dummy_file_input, dummy_config):
    response = json.load(open(FILE_PATH_INVOICE_V3_COMPLETE))
    parsed_response = PredictResponse[InvoiceV3](
        doc_config=dummy_config[(OTS_OWNER, InvoiceV3.__name__)],
        http_response=response,
        input_source=dummy_file_input,
        response_ok=True,
    )
    assert isinstance(parsed_response.document, InvoiceV3)
    for page in parsed_response.pages:
        assert isinstance(page, InvoiceV3)


def test_response_receipt_v3(dummy_file_input, dummy_config):
    response = json.load(open(FILE_PATH_RECEIPT_V3_COMPLETE))
    parsed_response = PredictResponse[ReceiptV3](
        doc_config=dummy_config[(OTS_OWNER, ReceiptV3.__name__)],
        http_response=response,
        input_source=dummy_file_input,
        response_ok=True,
    )
    assert isinstance(parsed_response.document, ReceiptV3)
    for page in parsed_response.pages:
        assert isinstance(page, ReceiptV3)


def test_response_receipt_v4(dummy_file_input, dummy_config):
    response = json.load(open(FILE_PATH_RECEIPT_V4_COMPLETE))
    parsed_response = PredictResponse[ReceiptV4](
        doc_config=dummy_config[(OTS_OWNER, ReceiptV4.__name__)],
        http_response=response,
        input_source=dummy_file_input,
        response_ok=True,
    )
    assert isinstance(parsed_response.document, ReceiptV4)
    for page in parsed_response.pages:
        assert isinstance(page, ReceiptV4)


def test_response_financial_doc_with_receipt(dummy_file_input, dummy_config):
    response = json.load(open(FILE_PATH_FINANCIAL_DOC_V1_RECEIPT))
    parsed_response = PredictResponse[FinancialDocumentV1](
        doc_config=dummy_config[(OTS_OWNER, FinancialDocumentV1.__name__)],
        http_response=response,
        input_source=dummy_file_input,
        response_ok=True,
    )
    assert isinstance(parsed_response.document, FinancialDocumentV1)
    for page in parsed_response.pages:
        assert isinstance(page, FinancialDocumentV1)


def test_response_passport_v1(dummy_file_input, dummy_config):
    response = json.load(open(FILE_PATH_PASSPORT_V1_COMPLETE))
    parsed_response = PredictResponse[PassportV1](
        doc_config=dummy_config[(OTS_OWNER, PassportV1.__name__)],
        http_response=response,
        input_source=dummy_file_input,
        response_ok=True,
    )
    assert isinstance(parsed_response.document, PassportV1)
    for page in parsed_response.pages:
        assert isinstance(page, PassportV1)
