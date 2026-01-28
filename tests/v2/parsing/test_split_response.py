import pytest

from mindee import LocalResponse
from mindee.v2.parsing.inference.split.split_inference import SplitInference
from mindee.v2.parsing.inference.split.split_response import SplitResponse
from tests.utils import V2_UTILITIES_DATA_DIR


@pytest.mark.v2
def test_split_single():
    input_inference = LocalResponse(V2_UTILITIES_DATA_DIR / "split_single.json")
    split_response = input_inference.deserialize_response(SplitResponse)
    assert isinstance(split_response.inference, SplitInference)
    assert split_response.inference.result.get("split")
    assert len(split_response.inference.result.get("split")[0].get("page_range")) == 2
    assert split_response.inference.result.get("split")[0].get("page_range")[0] == 0
    assert split_response.inference.result.get("split")[0].get("page_range")[1] == 0
    assert (
        split_response.inference.result.get("split")[0].get("document_type")
        == "receipt"
    )


@pytest.mark.v2
def test_split_multiple():
    input_inference = LocalResponse(V2_UTILITIES_DATA_DIR / "split_multiple.json")
    split_response = input_inference.deserialize_response(SplitResponse)
    assert isinstance(split_response.inference, SplitInference)
    assert split_response.inference.result.get("split")
    assert len(split_response.inference.result.get("split")) == 3

    assert len(split_response.inference.result.get("split")[0].get("page_range")) == 2
    assert split_response.inference.result.get("split")[0].get("page_range")[0] == 0
    assert split_response.inference.result.get("split")[0].get("page_range")[1] == 0
    assert (
        split_response.inference.result.get("split")[0].get("document_type")
        == "invoice"
    )

    assert len(split_response.inference.result.get("split")[1].get("page_range")) == 2
    assert split_response.inference.result.get("split")[1].get("page_range")[0] == 1
    assert split_response.inference.result.get("split")[1].get("page_range")[1] == 3
    assert (
        split_response.inference.result.get("split")[1].get("document_type")
        == "invoice"
    )

    assert len(split_response.inference.result.get("split")[2].get("page_range")) == 2
    assert split_response.inference.result.get("split")[2].get("page_range")[0] == 4
    assert split_response.inference.result.get("split")[2].get("page_range")[1] == 4
    assert (
        split_response.inference.result.get("split")[2].get("document_type")
        == "invoice"
    )
