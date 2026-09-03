import json

import pytest

from mindee.v1.parsing.common.async_predict_response import AsyncPredictResponse
from mindee.v1.product.international_id import InternationalIdV2
from tests.utils import V1_EXTRAS_DIR


@pytest.fixture
def load_document():
    with open(V1_EXTRAS_DIR / "full_text_ocr/complete.json") as file:
        prediction_data = json.load(file)

    return AsyncPredictResponse(InternationalIdV2, prediction_data).document


def test_get_full_text_ocr_result(load_document):
    expected_text = (V1_EXTRAS_DIR / "full_text_ocr/full_text_ocr.txt").read_text()

    full_text_ocr = load_document.extras.full_text_ocr

    assert expected_text.strip() == str(full_text_ocr)
