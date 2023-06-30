import json

from mindee.documents import CustomV1
from mindee.documents.custom.line_items import get_line_items
from tests import CUSTOM_DATA_DIR


def test_line_items():
    json_data_path = f"{CUSTOM_DATA_DIR}/response_v1/line_items/single_table_01.json"
    json_data = json.load(open(json_data_path, "r"))
    doc = CustomV1(
        "field_test", api_prediction=json_data["document"]["inference"], page_n=None
    )
    anchors = ["beneficiary_birth_date"]
    columns = [
        "beneficiary_name",
        "beneficiary_birth_date",
        "beneficiary_rank",
        "beneficiary_number",
    ]
    fields = json_data["document"]["inference"]["prediction"]
    line_items = get_line_items(anchors, columns, fields)
    assert line_items[0]["beneficiary_name"]["content"] == "JAMES BOND 007"
    assert line_items[1]["beneficiary_name"]["content"] == "HARRY POTTER"
    assert line_items[2]["beneficiary_name"]["content"] == "DRAGO MALFOY"
