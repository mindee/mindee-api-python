import json

from mindee.parsing.common.document import Document
from mindee.parsing.custom import get_line_items
from mindee.product import CustomV1


def test_single_table_01():
    json_data_path = (
        f"./tests/data/products/custom/response_v1/line_items/single_table_01.json"
    )
    json_data = json.load(open(json_data_path, "r"))
    doc = Document(CustomV1, json_data["document"]).inference.prediction
    anchors = ["beneficiary_birth_date"]
    columns = [
        "beneficiary_name",
        "beneficiary_birth_date",
        "beneficiary_rank",
        "beneficiary_number",
    ]
    line_items = get_line_items(anchors, columns, doc.fields)
    assert len(line_items) == 3
    assert line_items[0].fields["beneficiary_name"].content == "JAMES BOND 007"
    assert line_items[0].fields["beneficiary_birth_date"].content == "1970-11-11"
    assert line_items[0].row_number == 0
    assert line_items[1].fields["beneficiary_name"].content == "HARRY POTTER"
    assert line_items[1].fields["beneficiary_birth_date"].content == "2010-07-18"
    assert line_items[1].row_number == 1
    assert line_items[2].fields["beneficiary_name"].content == "DRAGO MALFOY"
    assert line_items[2].fields["beneficiary_birth_date"].content == "2015-07-05"
    assert line_items[2].row_number == 2
