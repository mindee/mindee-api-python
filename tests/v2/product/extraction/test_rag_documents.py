import json

import pytest

from mindee.v2.product.extraction.rag_documents import ExtractionRagAnnotationResponse
from mindee.v2.product.extraction.rag_documents.annotated_list_field import (
    AnnotatedListField,
)
from mindee.v2.product.extraction.rag_documents.annotated_object_field import (
    AnnotatedObjectField,
)
from mindee.v2.product.extraction.rag_documents.annotated_simple_field import (
    AnnotatedSimpleField,
)
from tests.utils import V2_PRODUCT_PATH


@pytest.mark.v2
def test_rag_documents_post_must_have_valid_properties():
    """Should load a POST response from a JSON string."""

    response = _get_response("extraction/rag_documents/post_response.json")
    assert response is not None
    assert response.id == "cc831599-c545-48b7-aa27-6d7ccd5b8d32"
    assert response.status == "Processing"
    assert response.annotation is None


@pytest.mark.v2
def test_rag_documents_get_draft_must_have_valid_properties():
    """Should load a GET response from a JSON string."""

    response = _get_response("extraction/rag_documents/get_response_draft.json")
    assert response is not None
    assert response.id == "cc831599-c545-48b7-aa27-6d7ccd5b8d32"
    assert response.status == "Draft"
    assert response.annotation is not None
    fields = response.annotation.fields
    assert fields is not None

    # null simple field
    tip_field = fields.get_simple_field("tip")
    assert isinstance(tip_field, AnnotatedSimpleField)
    assert tip_field.selected is False
    assert tip_field.guidelines is None
    assert tip_field.value is None

    # filled simple field
    date_field = fields.get_simple_field("date")
    assert isinstance(date_field, AnnotatedSimpleField)
    assert date_field.selected is False
    assert date_field.guidelines is None
    assert date_field.value == "2019-11-02"

    # filled object field
    locale_field = fields.get_object_field("locale")
    assert isinstance(locale_field, AnnotatedObjectField)
    assert locale_field.selected is False
    assert locale_field.guidelines is None
    assert locale_field.fields is not None
    assert len(locale_field.fields) == 3
    assert locale_field.get_simple_field("country").value == "US"
    assert locale_field.get_simple_field("currency").value == "USD"
    assert locale_field.get_simple_field("language").value is None

    # list of simple fields
    reference_numbers_field = fields.get_list_field("reference_numbers")
    assert isinstance(reference_numbers_field, AnnotatedListField)
    assert reference_numbers_field.selected is False
    assert reference_numbers_field.guidelines is None
    assert reference_numbers_field.items is not None
    assert len(reference_numbers_field.items) == 1
    assert reference_numbers_field.simple_items[0].value == "2412/2019"

    # list of object fields
    line_items_field = fields.get_list_field("line_items")
    assert isinstance(line_items_field, AnnotatedListField)
    assert line_items_field.selected is False
    assert line_items_field.guidelines is None
    assert line_items_field.items is not None
    assert len(line_items_field.items) == 3

    line_item_0 = line_items_field.object_items[0]
    assert line_item_0.fields is not None
    assert len(line_item_0.fields) == 8
    assert line_item_0.fields["description"].value == "Front and rear brake cables"
    assert line_item_0.fields["quantity"].value == 1
    assert line_item_0.fields["unit_price"].value == 100
    assert line_item_0.fields["total_price"].value == 100
    assert line_item_0.fields["tax_rate"].value is None
    assert line_item_0.fields["tax_amount"].value is None
    assert line_item_0.fields["product_code"].value is None
    assert line_item_0.fields["unit_measure"].value is None

    line_item_1 = line_items_field.object_items[1]
    assert line_item_1.fields is not None
    assert len(line_item_1.fields) == 8
    assert line_item_1.fields["description"].value == "New set of pedal arms"
    assert line_item_1.fields["quantity"].value == 2
    assert line_item_1.fields["unit_price"].value == 25
    assert line_item_1.fields["total_price"].value == 50
    assert line_item_1.fields["tax_rate"].value is None
    assert line_item_1.fields["tax_amount"].value is None
    assert line_item_1.fields["product_code"].value is None
    assert line_item_1.fields["unit_measure"].value is None

    line_item_2 = line_items_field.object_items[2]
    assert line_item_2.fields is not None
    assert len(line_item_2.fields) == 8
    assert line_item_2.fields["description"].value == "Labor 3hrs"
    assert line_item_2.fields["quantity"].value == 3
    assert line_item_2.fields["unit_price"].value == 15
    assert line_item_2.fields["total_price"].value == 45
    assert line_item_2.fields["tax_rate"].value is None
    assert line_item_2.fields["tax_amount"].value is None
    assert line_item_2.fields["product_code"].value is None
    assert line_item_2.fields["unit_measure"].value is None


def _get_response(path: str) -> ExtractionRagAnnotationResponse:
    file_path = V2_PRODUCT_PATH / path
    with open(file_path, encoding="utf-8") as f:
        response_dict = json.load(f)
    return ExtractionRagAnnotationResponse(response_dict)
