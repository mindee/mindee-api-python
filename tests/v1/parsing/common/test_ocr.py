import json

from mindee.v1.parsing.common import OCR
from tests.utils import V1_DATA_DIR


def test_response():
    with open(V1_DATA_DIR / "extras" / "ocr" / "complete.json") as json_file:
        json_data = json.load(json_file)
    with open(V1_DATA_DIR / "extras" / "ocr" / "ocr.txt") as file_handle:
        expected_text = file_handle.read()
    ocr = OCR(json_data["document"]["ocr"])
    assert str(ocr) == expected_text
    assert str(ocr.mvision_v1.pages[0]) == expected_text
