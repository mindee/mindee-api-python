import json

import pytest

from mindee.parsing.common.document import Document
from mindee.product import InvoiceSplitterV1

INVOICE_SPLITTER_DATA_DIR = "./tests/data/products/invoice_splitter"
FILE_PATH_INVOICE_SPLITTER_V1_COMPLETE = (
    f"{ INVOICE_SPLITTER_DATA_DIR }/response_v1/complete.json"
)
FILE_PATH_INVOICE_SPLITTER_V1_EMPTY = (
    f"{ INVOICE_SPLITTER_DATA_DIR }/response_v1/empty.json"
)
FILE_PATH_SUMMARY_FULL = f"{INVOICE_SPLITTER_DATA_DIR}/response_v1/summary_full.rst"


@pytest.fixture
def invoice_splitter_v1_complete_doc():
    json_data = json.load(open(FILE_PATH_INVOICE_SPLITTER_V1_COMPLETE))
    return Document(InvoiceSplitterV1, json_data["document"])


@pytest.fixture
def invoice_splitter_v1_empty_doc():
    json_data = json.load(open(FILE_PATH_INVOICE_SPLITTER_V1_EMPTY))
    return Document(InvoiceSplitterV1, json_data["document"])


def test_complete_doc(
    invoice_splitter_v1_complete_doc,
):
    file_path = FILE_PATH_SUMMARY_FULL
    reference_str = open(file_path, "r", encoding="utf-8").read()
    assert (
        len(invoice_splitter_v1_complete_doc.inference.prediction.invoice_page_groups)
        == 3
    )
    assert (
        invoice_splitter_v1_complete_doc.inference.prediction.invoice_page_groups[
            0
        ].confidence
        == 1
    )
    assert (
        invoice_splitter_v1_complete_doc.inference.prediction.invoice_page_groups[
            2
        ].confidence
        == 0
    )
    assert str(invoice_splitter_v1_complete_doc) == reference_str


def test_empty_doc(invoice_splitter_v1_empty_doc):
    assert (
        len(invoice_splitter_v1_empty_doc.inference.prediction.invoice_page_groups) == 0
    )
