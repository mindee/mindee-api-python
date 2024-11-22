import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1 import (
    NutritionFactsLabelV1,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_document import (
    NutritionFactsLabelV1Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "nutrition_facts" / "response_v1"

NutritionFactsLabelV1DocumentType = Document[
    NutritionFactsLabelV1Document,
    Page[NutritionFactsLabelV1Document],
]


@pytest.fixture
def complete_doc() -> NutritionFactsLabelV1DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(NutritionFactsLabelV1, json_data["document"])


@pytest.fixture
def empty_doc() -> NutritionFactsLabelV1DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(NutritionFactsLabelV1, json_data["document"])


def test_complete_doc(complete_doc: NutritionFactsLabelV1DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: NutritionFactsLabelV1DocumentType):
    prediction = empty_doc.inference.prediction
    assert prediction.serving_per_box.value is None
    assert prediction.serving_size.amount is None
    assert prediction.serving_size.unit is None
    assert prediction.calories.daily_value is None
    assert prediction.calories.per_100g is None
    assert prediction.calories.per_serving is None
    assert prediction.total_fat.daily_value is None
    assert prediction.total_fat.per_100g is None
    assert prediction.total_fat.per_serving is None
    assert prediction.saturated_fat.daily_value is None
    assert prediction.saturated_fat.per_100g is None
    assert prediction.saturated_fat.per_serving is None
    assert prediction.trans_fat.daily_value is None
    assert prediction.trans_fat.per_100g is None
    assert prediction.trans_fat.per_serving is None
    assert prediction.cholesterol.daily_value is None
    assert prediction.cholesterol.per_100g is None
    assert prediction.cholesterol.per_serving is None
    assert prediction.total_carbohydrate.daily_value is None
    assert prediction.total_carbohydrate.per_100g is None
    assert prediction.total_carbohydrate.per_serving is None
    assert prediction.dietary_fiber.daily_value is None
    assert prediction.dietary_fiber.per_100g is None
    assert prediction.dietary_fiber.per_serving is None
    assert prediction.total_sugars.daily_value is None
    assert prediction.total_sugars.per_100g is None
    assert prediction.total_sugars.per_serving is None
    assert prediction.added_sugars.daily_value is None
    assert prediction.added_sugars.per_100g is None
    assert prediction.added_sugars.per_serving is None
    assert prediction.protein.daily_value is None
    assert prediction.protein.per_100g is None
    assert prediction.protein.per_serving is None
    assert prediction.sodium.daily_value is None
    assert prediction.sodium.per_100g is None
    assert prediction.sodium.per_serving is None
    assert prediction.sodium.unit is None
    assert len(prediction.nutrients) == 0
