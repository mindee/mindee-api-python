import pytest

from mindee.input.path_input import PathInput
from mindee.v2 import SplitParameters, SplitResponse
from mindee.v2.client import Client
from tests.utils import V2_PRODUCT_PATH


@pytest.mark.integration
@pytest.mark.v2
def test_split_default_sample(v2_client: Client, split_model_id: str):
    input_source = PathInput(V2_PRODUCT_PATH / "split" / "default_sample.pdf")
    response = v2_client.enqueue_and_get_result(
        SplitResponse, input_source, SplitParameters(split_model_id)
    )
    assert response.inference is not None
    assert response.inference.file.name == "default_sample.pdf"
    assert response.inference.result.splits
    assert len(response.inference.result.splits) == 2
