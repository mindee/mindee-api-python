import pytest

from mindee import LocalResponse
from mindee.v2.parsing import ErrorResponse
from tests.utils import V2_RESOURCE_PATH


@pytest.mark.v2
def test_rst_output_must_be_valid():
    """Should load and pretty print an error response."""

    local_response = LocalResponse(
        V2_RESOURCE_PATH / "errors/error_422_invalid_fields.json"
    )
    response = local_response.deserialize_response(ErrorResponse)

    with open(V2_RESOURCE_PATH / "errors/error_422_invalid_fields.rst") as rst_file:
        rst_output = rst_file.read()

    assert response
    assert str(response) == rst_output
