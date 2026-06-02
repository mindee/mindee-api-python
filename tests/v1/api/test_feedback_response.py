import json

from mindee.v1.parsing.common.feedback_response import FeedbackResponse
from tests.utils import V1_PRODUCT_DATA_DIR


def test_empty_feedback_response():
    with open(
        V1_PRODUCT_DATA_DIR / "invoices" / "feedback_response" / "empty.json"
    ) as json_file:
        response = json.load(json_file)
    feedback_response = FeedbackResponse(response)
    assert feedback_response is not None
    assert feedback_response.feedback["customer_address"] is None
