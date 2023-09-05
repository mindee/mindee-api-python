import json

import pytest

from mindee.documents import InvoiceSplitterV1

INVOICE_SPLITTER_DATA_DIR = "./tests/data/products/invoice_splitter"
FILE_PATH_INVOICE_SPLITTER_V1_COMPLETE = (
    f"{ INVOICE_SPLITTER_DATA_DIR }/response_v1/complete.json"
)
FILE_PATH_INVOICE_SPLITTER_V1_EMPTY = (
    f"{ INVOICE_SPLITTER_DATA_DIR }/response_v1/empty.json"
)


@pytest.fixture
def invoice_splitter_v1_doc() -> InvoiceSplitterV1:
    json_data = json.load(open(FILE_PATH_INVOICE_SPLITTER_V1_COMPLETE))
    return InvoiceSplitterV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def invoice_splitter_v1_doc_empty() -> InvoiceSplitterV1:
    json_data = json.load(open(FILE_PATH_INVOICE_SPLITTER_V1_EMPTY))
    return InvoiceSplitterV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def invoice_splitter_v1_page_object():
    json_data = json.load(open(FILE_PATH_INVOICE_SPLITTER_V1_COMPLETE))
    return InvoiceSplitterV1(json_data["document"]["inference"]["pages"][0], page_n=0)


@pytest.fixture
def invoice_splitter_v1_doc_object():
    json_data = json.load(open(FILE_PATH_INVOICE_SPLITTER_V1_COMPLETE))
    return InvoiceSplitterV1(json_data["document"]["inference"], page_n=0)


def test_doc_constructor(invoice_splitter_v1_doc):
    file_path = f"{ INVOICE_SPLITTER_DATA_DIR }/response_v1/doc_to_string.rst"
    reference_str = open(file_path, "r", encoding="utf-8").read()
    assert str(invoice_splitter_v1_doc) == reference_str
