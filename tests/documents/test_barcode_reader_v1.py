import json

import pytest

from mindee.documents import BarcodeReaderV1

BARCODE_READER_DATA_DIR = "./tests/data/products/barcode_reader"
FILE_PATH_BARCODE_READER_V1_COMPLETE = (
    f"{ BARCODE_READER_DATA_DIR }/response_v1/complete.json"
)
FILE_PATH_BARCODE_READER_V1_EMPTY = (
    f"{ BARCODE_READER_DATA_DIR }/response_v1/empty.json"
)


@pytest.fixture
def barcode_reader_v1_doc() -> BarcodeReaderV1:
    json_data = json.load(open(FILE_PATH_BARCODE_READER_V1_COMPLETE, encoding="utf-8"))
    return BarcodeReaderV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def barcode_reader_v1_doc_empty() -> BarcodeReaderV1:
    json_data = json.load(open(FILE_PATH_BARCODE_READER_V1_EMPTY, encoding="utf-8"))
    return BarcodeReaderV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def barcode_reader_v1_page0():
    json_data = json.load(open(FILE_PATH_BARCODE_READER_V1_COMPLETE, encoding="utf-8"))
    return BarcodeReaderV1(json_data["document"]["inference"]["pages"][0], page_n=0)


def test_empty_doc_constructor(barcode_reader_v1_doc_empty):
    assert len(barcode_reader_v1_doc_empty.codes_1d) == 0
    assert len(barcode_reader_v1_doc_empty.codes_2d) == 0
