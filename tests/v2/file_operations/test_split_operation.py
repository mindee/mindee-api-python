import json

import pytest

from mindee.input.path_input import PathInput
from mindee.v2.product.split.split_response import (
    SplitResponse,
)
from tests.utils import V2_PRODUCT_DATA_DIR


@pytest.fixture
def splits_5p():
    return V2_PRODUCT_DATA_DIR / "split" / "invoice_5p.pdf"


@pytest.fixture
def splits_single_page_json_path():
    return V2_PRODUCT_DATA_DIR / "split" / "split_single.json"


@pytest.fixture
def splits_multi_page_json_path():
    return V2_PRODUCT_DATA_DIR / "split" / "split_multiple.json"


@pytest.mark.bernard_ledit
def test_default_split():
    input_sample = PathInput(V2_PRODUCT_DATA_DIR / "split" / "default_sample.pdf")
    with open(V2_PRODUCT_DATA_DIR / "split" / "default_sample.json", "rb") as f:
        response = SplitResponse(json.load(f))
    extracted_splits = response.inference.result.extract_from_input_source(input_sample)
    assert len(extracted_splits) == 2

    assert extracted_splits[0].page_count == 1
    assert extracted_splits[0].filename == "default_sample_pages-001-001.pdf"
    assert extracted_splits[1].page_count == 1
    assert extracted_splits[1].filename == "default_sample_pages-002-002.pdf"


@pytest.mark.bernard_ledit
def test_multi_page_receipt_split(splits_5p, splits_multi_page_json_path):
    input_sample = PathInput(splits_5p)
    with open(splits_multi_page_json_path, "rb") as f:
        response = SplitResponse(json.load(f))
    extracted_splits = response.inference.result.extract_from_input_source(input_sample)
    assert len(extracted_splits) == 3

    assert extracted_splits[0].page_count == 1
    assert extracted_splits[0].page_indexes == [0]
    assert extracted_splits[0].filename == "invoice_5p_pages-001-001.pdf"
    assert extracted_splits[1].page_count == 3
    assert extracted_splits[1].page_indexes == [1, 2, 3]
    assert extracted_splits[1].filename == "invoice_5p_pages-002-004.pdf"
    assert extracted_splits[2].page_count == 1
    assert extracted_splits[2].page_indexes == [4]
    assert extracted_splits[2].filename == "invoice_5p_pages-005-005.pdf"


@pytest.mark.bernard_ledit
def test_multi_page_receipt_single_split(splits_5p, splits_multi_page_json_path):
    input_sample = PathInput(splits_5p)
    with open(splits_multi_page_json_path, "rb") as f:
        response = SplitResponse(json.load(f))
    split = response.inference.result.splits[1]
    extracted_split = split.extract_from_input_source(input_sample)

    assert extracted_split.page_count == 3
