import json

import pytest

from mindee.documents import MultiReceiptsDetectorV1

MULTI_RECEIPTS_DETECTOR_DATA_DIR = "./tests/data/products/multi_receipts_detector"
FILE_PATH_MULTI_RECEIPTS_DETECTOR_V1_COMPLETE = (
    f"{ MULTI_RECEIPTS_DETECTOR_DATA_DIR }/response_v1/complete.json"
)
FILE_PATH_MULTI_RECEIPTS_DETECTOR_V1_EMPTY = (
    f"{ MULTI_RECEIPTS_DETECTOR_DATA_DIR }/response_v1/empty.json"
)


@pytest.fixture
def multi_receipts_detector_v1_doc() -> MultiReceiptsDetectorV1:
    json_data = json.load(
        open(FILE_PATH_MULTI_RECEIPTS_DETECTOR_V1_COMPLETE, encoding="utf-8")
    )
    return MultiReceiptsDetectorV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def multi_receipts_detector_v1_doc_empty() -> MultiReceiptsDetectorV1:
    json_data = json.load(
        open(FILE_PATH_MULTI_RECEIPTS_DETECTOR_V1_EMPTY, encoding="utf-8")
    )
    return MultiReceiptsDetectorV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def multi_receipts_detector_v1_page0():
    json_data = json.load(
        open(FILE_PATH_MULTI_RECEIPTS_DETECTOR_V1_COMPLETE, encoding="utf-8")
    )
    return MultiReceiptsDetectorV1(
        json_data["document"]["inference"]["pages"][0], page_n=0
    )


def test_empty_doc_constructor(multi_receipts_detector_v1_doc_empty):
    assert len(multi_receipts_detector_v1_doc_empty.receipts) == 0
