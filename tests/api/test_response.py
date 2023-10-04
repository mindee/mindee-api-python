import json

import pytest

from mindee import Client
from mindee.client import OTS_OWNER
from mindee.input.sources import PathInput
from mindee.parsing.common.document import Document
from mindee.parsing.common.predict_response import PredictResponse
from mindee.product import (  # FinancialDocumentV1,; InvoiceV3,; PassportV1,; ReceiptV3,
    ReceiptV4,
)


@pytest.fixture
def dummy_file_input():
    file_input = PathInput("./tests/data/file_types/receipt.jpg")
    return file_input


@pytest.fixture
def dummy_config():
    client = Client(api_key="dummy").create_endpoint(
        endpoint_name="dummy",
        account_name="dummy",
    )
    return client._doc_configs


def test_constructor(dummy_file_input):
    with pytest.raises(KeyError):
        Document(
            dummy_file_input, document_type="receipt", api_prediction={}, page_id=0
        )


# def test_response_receipt_v4(dummy_file_input, dummy_config):
#     response = json.load(open(FILE_PATH_RECEIPT_V4_COMPLETE))
#     parsed_response = PredictResponse[ReceiptV4](
#         doc_config=dummy_config[(OTS_OWNER, ReceiptV4.__name__)],
#         http_response=response,
#         input_source=dummy_file_input,
#         response_ok=True,
#     )
#     assert isinstance(parsed_response.document, ReceiptV4)
#     for page in parsed_response.pages:
#         assert isinstance(page, ReceiptV4)


# def test_response_financial_doc_with_receipt(dummy_file_input, dummy_config):
#     response = json.load(open(FILE_PATH_FINANCIAL_DOC_V1_RECEIPT))
#     parsed_response = PredictResponse[FinancialDocumentV1](
#         doc_config=dummy_config[(OTS_OWNER, FinancialDocumentV1.__name__)],
#         http_response=response,
#         input_source=dummy_file_input,
#         response_ok=True,
#     )
#     assert isinstance(parsed_response.document, FinancialDocumentV1)
#     for page in parsed_response.pages:
#         assert isinstance(page, FinancialDocumentV1)


# def test_response_passport_v1(dummy_file_input, dummy_config):
#     response = json.load(open(FILE_PATH_PASSPORT_V1_COMPLETE))
#     parsed_response = PredictResponse[PassportV1](
#         doc_config=dummy_config[(OTS_OWNER, PassportV1.__name__)],
#         http_response=response,
#         input_source=dummy_file_input,
#         response_ok=True,
#     )
#     assert isinstance(parsed_response.document, PassportV1)
#     for page in parsed_response.pages:
#         assert isinstance(page, PassportV1)
