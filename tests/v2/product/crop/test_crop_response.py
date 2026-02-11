import pytest

from mindee import LocalResponse
from mindee.v2.product.crop.crop_box import CropBox
from mindee.v2.product.crop import CropInference
from mindee.v2.product.crop.crop_response import CropResponse
from mindee.v2.product.crop.crop_result import CropResult
from tests.utils import V2_PRODUCT_DATA_DIR


@pytest.mark.v2
def test_crop_single():
    input_inference = LocalResponse(V2_PRODUCT_DATA_DIR / "crop" / "crop_single.json")
    crop_response = input_inference.deserialize_response(CropResponse)
    assert isinstance(crop_response.inference, CropInference)
    assert crop_response.inference.result.crops
    assert len(crop_response.inference.result.crops[0].location.polygon) == 4
    assert crop_response.inference.result.crops[0].location.polygon[0][0] == 0.15
    assert crop_response.inference.result.crops[0].location.polygon[0][1] == 0.254
    assert crop_response.inference.result.crops[0].location.polygon[1][0] == 0.85
    assert crop_response.inference.result.crops[0].location.polygon[1][1] == 0.254
    assert crop_response.inference.result.crops[0].location.polygon[2][0] == 0.85
    assert crop_response.inference.result.crops[0].location.polygon[2][1] == 0.947
    assert crop_response.inference.result.crops[0].location.polygon[3][0] == 0.15
    assert crop_response.inference.result.crops[0].location.polygon[3][1] == 0.947
    assert crop_response.inference.result.crops[0].location.page == 0
    assert crop_response.inference.result.crops[0].object_type == "invoice"


@pytest.mark.v2
def test_crop_multiple():
    input_inference = LocalResponse(V2_PRODUCT_DATA_DIR / "crop" / "crop_multiple.json")
    crop_response = input_inference.deserialize_response(CropResponse)
    assert isinstance(crop_response.inference, CropInference)
    assert isinstance(crop_response.inference.result, CropResult)
    assert isinstance(crop_response.inference.result.crops[0], CropBox)
    assert len(crop_response.inference.result.crops) == 2

    assert len(crop_response.inference.result.crops[0].location.polygon) == 4
    assert crop_response.inference.result.crops[0].location.polygon[0][0] == 0.214
    assert crop_response.inference.result.crops[0].location.polygon[0][1] == 0.079
    assert crop_response.inference.result.crops[0].location.polygon[1][0] == 0.476
    assert crop_response.inference.result.crops[0].location.polygon[1][1] == 0.079
    assert crop_response.inference.result.crops[0].location.polygon[2][0] == 0.476
    assert crop_response.inference.result.crops[0].location.polygon[2][1] == 0.979
    assert crop_response.inference.result.crops[0].location.polygon[3][0] == 0.214
    assert crop_response.inference.result.crops[0].location.polygon[3][1] == 0.979
    assert crop_response.inference.result.crops[0].location.page == 0
    assert crop_response.inference.result.crops[0].object_type == "invoice"

    assert len(crop_response.inference.result.crops[1].location.polygon) == 4
    assert crop_response.inference.result.crops[1].location.polygon[0][0] == 0.547
    assert crop_response.inference.result.crops[1].location.polygon[0][1] == 0.15
    assert crop_response.inference.result.crops[1].location.polygon[1][0] == 0.862
    assert crop_response.inference.result.crops[1].location.polygon[1][1] == 0.15
    assert crop_response.inference.result.crops[1].location.polygon[2][0] == 0.862
    assert crop_response.inference.result.crops[1].location.polygon[2][1] == 0.97
    assert crop_response.inference.result.crops[1].location.polygon[3][0] == 0.547
    assert crop_response.inference.result.crops[1].location.polygon[3][1] == 0.97
    assert crop_response.inference.result.crops[1].location.page == 0
    assert crop_response.inference.result.crops[1].object_type == "invoice"
