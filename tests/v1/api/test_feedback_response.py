import json

from mindee.parsing.common.feedback_response import FeedbackResponse
from tests.utils import V1_PRODUCT_DATA_DIR


def test_empty_feedback_response():
    response = json.load(
        open(V1_PRODUCT_DATA_DIR / "invoices" / "feedback_response" / "empty.json")
    )
    feedback_response = FeedbackResponse(response)
    assert feedback_response is not None
    assert feedback_response.feedback["customer_address"] is None
