import json

import pytest

from mindee.documents import ShippingContainerV1

SHIPPING_CONTAINER_DATA_DIR = "./tests/data/shipping_container"

FILE_PATH_SHIPPING_CONTAINER_V1_COMPLETE = (
    f"{ SHIPPING_CONTAINER_DATA_DIR }/response_v1/complete.json"
)
FILE_PATH_SHIPPING_CONTAINER_V1_EMPTY = (
    f"{ SHIPPING_CONTAINER_DATA_DIR }/response_v1/empty.json"
)


@pytest.fixture
def shipping_container_v1_doc() -> ShippingContainerV1:
    json_data = json.load(open(FILE_PATH_SHIPPING_CONTAINER_V1_COMPLETE))
    return ShippingContainerV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def shipping_container_v1_doc_empty() -> ShippingContainerV1:
    json_data = json.load(open(FILE_PATH_SHIPPING_CONTAINER_V1_EMPTY))
    return ShippingContainerV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def shipping_container_v1_page0():
    json_data = json.load(open(FILE_PATH_SHIPPING_CONTAINER_V1_COMPLETE))
    return ShippingContainerV1(json_data["document"]["inference"]["pages"][0], page_n=0)


def test_doc_constructor(shipping_container_v1_doc):
    file_path = f"{ SHIPPING_CONTAINER_DATA_DIR }/response_v1/doc_to_string.txt"
    reference_str = open(file_path, "r", encoding="utf-8").read().strip()
    assert str(shipping_container_v1_doc) == reference_str


def test_page0_constructor(shipping_container_v1_page0):
    file_path = f"{ SHIPPING_CONTAINER_DATA_DIR }/response_v1/page0_to_string.txt"
    reference_str = open(file_path, "r", encoding="utf-8").read().strip()
    assert str(shipping_container_v1_page0) == reference_str
