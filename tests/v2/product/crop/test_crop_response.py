import pytest

from mindee import ExtractionResponse
from mindee.v2.product.crop.crop_box import CropBox
from mindee.v2.product.crop import CropInference
from mindee.v2.product.crop.crop_response import CropResponse
from mindee.v2.product.crop.crop_result import CropResult

from tests.v2.product.utils import get_product_samples


@pytest.mark.v2
def test_crop_single():
    json_sample, rst_sample = get_product_samples(
        product="crop", file_name="crop_single"
    )
    response = CropResponse(json_sample)
    assert isinstance(response.inference, CropInference)
    assert response.inference.result.crops
    assert len(response.inference.result.crops[0].location.polygon) == 4
    assert response.inference.result.crops[0].location.polygon[0][0] == 0.15
    assert response.inference.result.crops[0].location.polygon[0][1] == 0.254
    assert response.inference.result.crops[0].location.polygon[1][0] == 0.85
    assert response.inference.result.crops[0].location.polygon[1][1] == 0.254
    assert response.inference.result.crops[0].location.polygon[2][0] == 0.85
    assert response.inference.result.crops[0].location.polygon[2][1] == 0.947
    assert response.inference.result.crops[0].location.polygon[3][0] == 0.15
    assert response.inference.result.crops[0].location.polygon[3][1] == 0.947
    assert response.inference.result.crops[0].location.page == 0
    assert response.inference.result.crops[0].object_type == "invoice"

    assert rst_sample == str(response)


@pytest.mark.v2
def test_crop_multiple():
    json_sample, rst_sample = get_product_samples(
        product="crop", file_name="crop_multiple"
    )
    response = CropResponse(json_sample)
    assert isinstance(response.inference, CropInference)
    assert isinstance(response.inference.result, CropResult)
    assert isinstance(response.inference.result.crops[0], CropBox)
    assert len(response.inference.result.crops) == 2

    assert len(response.inference.result.crops[0].location.polygon) == 4
    assert response.inference.result.crops[0].location.polygon[0][0] == 0.214
    assert response.inference.result.crops[0].location.polygon[0][1] == 0.079
    assert response.inference.result.crops[0].location.polygon[1][0] == 0.476
    assert response.inference.result.crops[0].location.polygon[1][1] == 0.079
    assert response.inference.result.crops[0].location.polygon[2][0] == 0.476
    assert response.inference.result.crops[0].location.polygon[2][1] == 0.979
    assert response.inference.result.crops[0].location.polygon[3][0] == 0.214
    assert response.inference.result.crops[0].location.polygon[3][1] == 0.979
    assert response.inference.result.crops[0].location.page == 0
    assert response.inference.result.crops[0].object_type == "invoice"

    assert len(response.inference.result.crops[1].location.polygon) == 4
    assert response.inference.result.crops[1].location.polygon[0][0] == 0.547
    assert response.inference.result.crops[1].location.polygon[0][1] == 0.15
    assert response.inference.result.crops[1].location.polygon[1][0] == 0.862
    assert response.inference.result.crops[1].location.polygon[1][1] == 0.15
    assert response.inference.result.crops[1].location.polygon[2][0] == 0.862
    assert response.inference.result.crops[1].location.polygon[2][1] == 0.97
    assert response.inference.result.crops[1].location.polygon[3][0] == 0.547
    assert response.inference.result.crops[1].location.polygon[3][1] == 0.97
    assert response.inference.result.crops[1].location.page == 0
    assert response.inference.result.crops[1].object_type == "receipt"

    assert rst_sample == str(response)


@pytest.mark.v2
def test_crop_with_extraction_result():
    json_sample, _ = get_product_samples(
        product="crop", file_name="default_sample_extraction"
    )
    response = CropResponse(json_sample)
    assert isinstance(response.inference, CropInference)
    assert isinstance(response.inference.result, CropResult)
    assert isinstance(
        response.inference.result.crops[0],
        CropBox,
    )
    crops = response.inference.result.crops
    assert crops[0].object_type == "receipt"
    assert isinstance(crops[0].extraction_response, ExtractionResponse)
    assert (
        crops[0].extraction_response.inference.result.fields.get("supplier_name").value
        == "CHEZ ALAIN MIAM MIAM"
    )

    assert crops[1].object_type == "receipt"
    assert isinstance(crops[1].extraction_response, ExtractionResponse)
    assert (
        crops[1].extraction_response.inference.result.fields.get("supplier_name").value
        == "La cerise sur la pizza"
    )
