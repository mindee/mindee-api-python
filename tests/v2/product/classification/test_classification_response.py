import pytest

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
        product="classification", file_name="classification_single"
    )
    response = ClassificationResponse(json_sample)
    assert isinstance(response.inference, ClassificationInference)
    assert isinstance(response.inference.result, ClassificationResult)
    assert isinstance(
        response.inference.result.classification,
        ClassificationClassifier,
    )
    assert response.inference.result.classification.document_type == "invoice"
