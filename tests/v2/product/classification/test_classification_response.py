import pytest

from mindee import LocalResponse
from mindee.v2.product.classification.classification_classifier import (
    ClassificationClassifier,
)
from mindee.v2.product.classification import ClassificationInference
from mindee.v2.product.classification.classification_response import (
    ClassificationResponse,
)
from mindee.v2.product.classification.classification_result import ClassificationResult
from tests.utils import V2_UTILITIES_DATA_DIR


@pytest.mark.v2
def test_classification_single():
    input_inference = LocalResponse(
        V2_UTILITIES_DATA_DIR / "classification" / "classification_single.json"
    )
    classification_response = input_inference.deserialize_response(
        ClassificationResponse
    )
    assert isinstance(classification_response.inference, ClassificationInference)
    assert isinstance(classification_response.inference.result, ClassificationResult)
    assert isinstance(
        classification_response.inference.result.classification,
        ClassificationClassifier,
    )
    assert (
        classification_response.inference.result.classification.document_type
        == "invoice"
    )
