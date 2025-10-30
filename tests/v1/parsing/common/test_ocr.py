import json

from mindee.parsing.common.ocr.ocr import Ocr


def test_response():
    json_data = json.load(open("./tests/data/extras/ocr/complete.json"))
    with open("./tests/data/extras/ocr/ocr.txt") as file_handle:
        expected_text = file_handle.read()
    ocr = Ocr(json_data["document"]["ocr"])
    assert str(ocr) == expected_text
    assert str(ocr.mvision_v1.pages[0]) == expected_text
