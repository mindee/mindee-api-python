import json

import pytest

from mindee.parsing.common.async_predict_response import AsyncPredictResponse
from mindee.product.international_id.international_id_v2 import InternationalIdV2
from tests.utils import EXTRAS_DIR

# NOTE: Implementing extras per pages without content (like the Java library)
# would be a breaking change for the Python SDK.
# This fixture is left here as a reminder that next major version should probably implement it.

# @pytest.fixture
# def load_pages():
#     with open(EXTRAS_DIR / "full_text_ocr/complete.json", "r") as file:
#         prediction_data = json.load(file)
#     return AsyncPredictResponse(InternationalIdV2, prediction_data).document.inference.pages


@pytest.fixture
def load_document():
    with open(EXTRAS_DIR / "full_text_ocr/complete.json", "r") as file:
        prediction_data = json.load(file)

    return AsyncPredictResponse(InternationalIdV2, prediction_data).document


def test_get_full_text_ocr_result(
    load_document,
    # load_pages
):
    expected_text = (EXTRAS_DIR / "full_text_ocr/full_text_ocr.txt").read_text()

    full_text_ocr = load_document.extras.full_text_ocr
    # page0_ocr = load_pages[0].extras.full_text_ocr.content

    assert expected_text.strip() == str(full_text_ocr)
    # assert "\n".join(expected_text) == page0_ocr
