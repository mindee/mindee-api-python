import json

import pytest

from mindee.v2.file_operations.split import Split
from mindee.input.sources.path_input import PathInput
from mindee.v2.product.split.split_response import (
    SplitResponse,
)
from tests.utils import V2_PRODUCT_DATA_DIR


@pytest.fixture
def splits_default():
    return (
        V2_PRODUCT_DATA_DIR / "extraction" / "financial_document" / "default_sample.jpg"
    )


@pytest.fixture
def splits_5p():
    return V2_PRODUCT_DATA_DIR / "split" / "invoice_5p.pdf"


@pytest.fixture
def splits_single_page_json_path():
    return V2_PRODUCT_DATA_DIR / "split" / "split_single.json"


@pytest.fixture
def splits_multi_page_json_path():
    return V2_PRODUCT_DATA_DIR / "split" / "split_multiple.json"


def test_single_page_split_split(splits_default, splits_single_page_json_path):
    input_sample = PathInput(splits_default)
    with open(splits_single_page_json_path, "rb") as f:
        response = json.load(f)
    doc = SplitResponse(response)
    extracted_splits = Split.extract_splits(input_sample, doc.inference.result.splits)
    assert len(extracted_splits) == 1

    assert extracted_splits[0].get_page_count() == 1


def test_multi_page_receipt_split(splits_5p, splits_multi_page_json_path):
    input_sample = PathInput(splits_5p)
    with open(splits_multi_page_json_path, "rb") as f:
        response = json.load(f)
    doc = SplitResponse(response)
    extracted_splits = Split.extract_splits(input_sample, doc.inference.result.splits)
    assert len(extracted_splits) == 3

    assert extracted_splits[0].get_page_count() == 1
    assert extracted_splits[1].get_page_count() == 3
    assert extracted_splits[2].get_page_count() == 1
