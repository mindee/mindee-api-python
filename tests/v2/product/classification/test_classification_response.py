import pytest

from mindee import ExtractionResponse
from mindee.v2.product.classification.classification_classifier import (
    ClassificationClassifier,
)
from mindee.v2.product.classification import ClassificationInference
from mindee.v2.product.classification.classification_response import (
    ClassificationResponse,
)
from mindee.v2.product.classification.classification_result import ClassificationResult
from tests.v2.product.utils import get_product_samples


@pytest.mark.v2
def test_classification_single():
    json_sample, _ = get_product_samples(
        product="classification", file_name="default_sample"
    )
    response = ClassificationResponse(json_sample)
    assert isinstance(response.inference, ClassificationInference)
    assert isinstance(response.inference.result, ClassificationResult)
    assert isinstance(
        response.inference.result.classification,
        ClassificationClassifier,
    )
    assert response.inference.result.classification.document_type == "invoice"


@pytest.mark.v2
def test_classification_with_extraction_result():
    json_sample, _ = get_product_samples(
        product="classification", file_name="default_sample_extraction"
    )
    response = ClassificationResponse(json_sample)
    assert isinstance(response.inference, ClassificationInference)
    assert isinstance(response.inference.result, ClassificationResult)
    assert isinstance(
        response.inference.result.classification,
        ClassificationClassifier,
    )
    classification = response.inference.result.classification
    assert classification.document_type == "invoice"
    assert isinstance(classification.extraction_response, ExtractionResponse)
    assert (
        classification.extraction_response.inference.result.fields.get(
            "customer_name"
        ).value
        == "Jiro Doi"
    )
