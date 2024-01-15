import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.parsing.generated.generated_list import GeneratedListField
from mindee.parsing.generated.generated_object import GeneratedObjectField
from mindee.parsing.standard.position import PositionField
from mindee.parsing.standard.text import StringField
from mindee.product.generated.generated_v1 import GeneratedV1
from mindee.product.generated.generated_v1_document import GeneratedV1Document
from mindee.product.generated.generated_v1_page import GeneratedV1Page
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def international_id_v1_complete_doc() -> (
    Document[GeneratedV1Document, Page[GeneratedV1Page]]
):
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR
            / "generated"
            / "response_v1"
            / "complete_international_id_v1.json",
            encoding="utf-8",
        )
    )
    return Document(GeneratedV1, json_data["document"])


@pytest.fixture
def international_id_v1_empty_doc() -> (
    Document[GeneratedV1Document, Page[GeneratedV1Page]]
):
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR
            / "generated"
            / "response_v1"
            / "empty_international_id_v1.json",
            encoding="utf-8",
        )
    )

    return Document(GeneratedV1, json_data["document"])


@pytest.fixture
def invoice_v4_empty_doc() -> Document[GeneratedV1Document, Page[GeneratedV1Page]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "generated" / "response_v1" / "empty_invoice_v4.json",
            encoding="utf-8",
        )
    )
    return Document(GeneratedV1, json_data["document"])


@pytest.fixture
def invoice_v4_complete_doc() -> Document[GeneratedV1Document, Page[GeneratedV1Page]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "generated" / "response_v1" / "complete_invoice_v4.json",
            encoding="utf-8",
        )
    )
    return Document(GeneratedV1, json_data["document"])


@pytest.fixture
def invoice_v4_page_0() -> Document[GeneratedV1Document, Page[GeneratedV1Page]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "generated" / "response_v1" / "complete_invoice_v4.json",
            encoding="utf-8",
        )
    )
    return Page(GeneratedV1Page, json_data["document"]["inference"]["pages"][0])


def test_international_id_v1_empty_doc(international_id_v1_empty_doc) -> None:
    doc_str = open(
        PRODUCT_DATA_DIR
        / "generated"
        / "response_v1"
        / "summary_empty_international_id_v1.rst",
        encoding="utf-8",
    ).read()
    assert str(international_id_v1_empty_doc) == doc_str


def test_international_id_v1_complete_doc(international_id_v1_complete_doc) -> None:
    doc_str = open(
        PRODUCT_DATA_DIR
        / "generated"
        / "response_v1"
        / "summary_full_international_id_v1.rst",
        encoding="utf-8",
    ).read()
    assert isinstance(
        international_id_v1_complete_doc.inference.prediction.fields["given_names"],
        GeneratedListField,
    )
    for (
        field
    ) in (
        international_id_v1_complete_doc.inference.prediction.get_list_fields().values()
    ):
        assert isinstance(field, GeneratedListField)
    for (
        field
    ) in (
        international_id_v1_complete_doc.inference.prediction.get_object_fields().values()
    ):
        assert isinstance(field, GeneratedObjectField)
    for (
        field
    ) in (
        international_id_v1_complete_doc.inference.prediction.get_single_fields().values()
    ):
        assert not isinstance(field, GeneratedObjectField)
        assert not isinstance(field, GeneratedListField)
    assert str(international_id_v1_complete_doc) == doc_str


def test_invoice_v4_complete_doc(invoice_v4_complete_doc) -> None:
    doc_str = open(
        PRODUCT_DATA_DIR / "generated" / "response_v1" / "summary_full_invoice_v4.rst",
        encoding="utf-8",
    ).read()
    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields["taxes"], GeneratedListField
    )
    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields["taxes"].values[0].polygon,
        PositionField,
    )
    assert [
        [point.x, point.y]
        for point in invoice_v4_complete_doc.inference.prediction.fields["taxes"]
        .values[0]
        .polygon.value
    ] == [[0.292, 0.749], [0.543, 0.749], [0.543, 0.763], [0.292, 0.763]]
    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields["line_items"],
        GeneratedListField,
    )
    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields["line_items"]
        .values[0]
        .polygon,
        PositionField,
    )
    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields["locale"],
        GeneratedObjectField,
    )
    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields["locale"].currency,
        str,
    )
    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields["document_type"],
        StringField,
    )
    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields[
            "supplier_company_registrations"
        ],
        GeneratedListField,
    )
    assert (
        len(
            invoice_v4_complete_doc.inference.prediction.fields[
                "supplier_company_registrations"
            ].values
        )
        == 0
    )
    for (
        field
    ) in invoice_v4_complete_doc.inference.prediction.get_list_fields().values():
        assert isinstance(field, GeneratedListField)
    for (
        field
    ) in invoice_v4_complete_doc.inference.prediction.get_object_fields().values():
        assert isinstance(field, GeneratedObjectField)
    for (
        field
    ) in invoice_v4_complete_doc.inference.prediction.get_single_fields().values():
        assert not isinstance(field, GeneratedObjectField)
        assert not isinstance(field, GeneratedListField)
    assert str(invoice_v4_complete_doc) == doc_str


def test_invoice_v4_page0(invoice_v4_page_0) -> None:
    doc_str = open(
        PRODUCT_DATA_DIR / "generated" / "response_v1" / "summary_page0_invoice_v4.rst",
        encoding="utf-8",
    ).read()
    assert str(invoice_v4_page_0) == doc_str


def test_invoice_v4_empty_doc(invoice_v4_empty_doc) -> None:
    doc_str = open(
        PRODUCT_DATA_DIR / "generated" / "response_v1" / "summary_empty_invoice_v4.rst",
        encoding="utf-8",
    ).read()
    assert str(invoice_v4_empty_doc) == doc_str
