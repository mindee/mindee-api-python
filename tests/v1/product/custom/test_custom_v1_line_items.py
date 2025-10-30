import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.custom.custom_v1 import CustomV1
from mindee.product.custom.custom_v1_page import CustomV1Page


@pytest.mark.lineitems
def do_tests(line_items):
    assert len(line_items) == 3
    assert line_items[0].fields["beneficiary_name"].content == "JAMES BOND 007"
    assert line_items[0].fields["beneficiary_birth_date"].content == "1970-11-11"
    assert line_items[0].row_number == 1
    assert line_items[1].fields["beneficiary_name"].content == "HARRY POTTER"
    assert line_items[1].fields["beneficiary_birth_date"].content == "2010-07-18"
    assert line_items[1].row_number == 2
    assert line_items[2].fields["beneficiary_name"].content == "DRAGO MALFOY"
    assert line_items[2].fields["beneficiary_birth_date"].content == "2015-07-05"
    assert line_items[2].row_number == 3


@pytest.mark.lineitems
def test_single_table_01():
    json_data_path = (
        "./tests/data/products/custom/response_v1/line_items/single_table_01.json"
    )
    json_data = json.load(open(json_data_path, "r"))
    doc = Document(CustomV1, json_data["document"]).inference.prediction
    page = Page(CustomV1Page, json_data["document"]["inference"]["pages"][0])
    anchors = ["beneficiary_name"]
    columns = [
        "beneficiary_birth_date",
        "beneficiary_number",
        "beneficiary_name",
        "beneficiary_rank",
    ]
    line_items = doc.columns_to_line_items(anchors, columns, 0.011)
    do_tests(line_items)
    line_items_page = page.prediction.columns_to_line_items(anchors, columns, 0.011)
    do_tests(line_items_page)


@pytest.mark.lineitems
def test_single_table_02():
    json_data_path = (
        "./tests/data/products/custom/response_v2/line_items/single_table_01.json"
    )
    json_data = json.load(open(json_data_path, "r"))
    doc = Document(CustomV1, json_data["document"]).inference.prediction
    page = Page(CustomV1Page, json_data["document"]["inference"]["pages"][0])
    anchors = ["beneficiary_name"]
    columns = [
        "beneficiary_birth_date",
        "beneficiary_number",
        "beneficiary_name",
        "beneficiary_rank",
    ]
    line_items = doc.columns_to_line_items(anchors, columns, 0.011)
    do_tests(line_items)
    line_items_page = page.prediction.columns_to_line_items(anchors, columns, 0.011)
    do_tests(line_items_page)
