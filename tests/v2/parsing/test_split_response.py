import pytest

from mindee import LocalResponse
from mindee.v2.product.split.split_range import SplitRange
from mindee.v2.product.split import SplitInference
from mindee.v2.product.split.split_response import SplitResponse
from mindee.v2.product.split.split_result import SplitResult
from tests.utils import V2_UTILITIES_DATA_DIR


@pytest.mark.v2
def test_split_single():
    input_inference = LocalResponse(V2_UTILITIES_DATA_DIR / "split_single.json")
    split_response = input_inference.deserialize_response(SplitResponse)
    assert isinstance(split_response.inference, SplitInference)
    assert split_response.inference.result.splits
    assert len(split_response.inference.result.splits[0].page_range) == 2
    assert split_response.inference.result.splits[0].page_range[0] == 0
    assert split_response.inference.result.splits[0].page_range[1] == 0
    assert split_response.inference.result.splits[0].document_type == "receipt"


@pytest.mark.v2
def test_split_multiple():
    input_inference = LocalResponse(V2_UTILITIES_DATA_DIR / "split_multiple.json")
    split_response = input_inference.deserialize_response(SplitResponse)
    assert isinstance(split_response.inference, SplitInference)
    assert isinstance(split_response.inference.result, SplitResult)
    assert isinstance(split_response.inference.result.splits[0], SplitRange)
    assert len(split_response.inference.result.splits) == 3

    assert len(split_response.inference.result.splits[0].page_range) == 2
    assert split_response.inference.result.splits[0].page_range[0] == 0
    assert split_response.inference.result.splits[0].page_range[1] == 0
    assert split_response.inference.result.splits[0].document_type == "invoice"

    assert len(split_response.inference.result.splits[1].page_range) == 2
    assert split_response.inference.result.splits[1].page_range[0] == 1
    assert split_response.inference.result.splits[1].page_range[1] == 3
    assert split_response.inference.result.splits[1].document_type == "invoice"

    assert len(split_response.inference.result.splits[2].page_range) == 2
    assert split_response.inference.result.splits[2].page_range[0] == 4
    assert split_response.inference.result.splits[2].page_range[1] == 4
    assert split_response.inference.result.splits[2].document_type == "invoice"
