import pytest

from mindee.v2.product.split.split_range import SplitRange
from mindee.v2.product.split import SplitInference
from mindee.v2.product.split.split_response import SplitResponse
from mindee.v2.product.split.split_result import SplitResult
from tests.v2.product.utils import get_product_samples


@pytest.mark.v2
def test_split_single():
    json_sample, _ = get_product_samples(product="split", file_name="split_single")
    response = SplitResponse(json_sample)

    assert isinstance(response.inference, SplitInference)
    assert response.inference.result.splits
    assert len(response.inference.result.splits[0].page_range) == 2
    assert response.inference.result.splits[0].page_range[0] == 0
    assert response.inference.result.splits[0].page_range[1] == 0
    assert response.inference.result.splits[0].document_type == "receipt"


@pytest.mark.v2
def test_split_multiple():
    json_sample, _ = get_product_samples(product="split", file_name="split_multiple")
    response = SplitResponse(json_sample)
    assert isinstance(response.inference, SplitInference)
    assert isinstance(response.inference.result, SplitResult)
    assert isinstance(response.inference.result.splits[0], SplitRange)
    assert len(response.inference.result.splits) == 3

    assert len(response.inference.result.splits[0].page_range) == 2
    assert response.inference.result.splits[0].page_range[0] == 0
    assert response.inference.result.splits[0].page_range[1] == 0
    assert response.inference.result.splits[0].document_type == "passport"

    assert len(response.inference.result.splits[1].page_range) == 2
    assert response.inference.result.splits[1].page_range[0] == 1
    assert response.inference.result.splits[1].page_range[1] == 3
    assert response.inference.result.splits[1].document_type == "invoice"

    assert len(response.inference.result.splits[2].page_range) == 2
    assert response.inference.result.splits[2].page_range[0] == 4
    assert response.inference.result.splits[2].page_range[1] == 4
    assert response.inference.result.splits[2].document_type == "receipt"
