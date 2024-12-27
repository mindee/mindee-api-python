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
    assert isinstance(
        international_id_v1_empty_doc.inference.prediction.fields["document_type"],
        StringField,
    )
    assert (
        international_id_v1_empty_doc.inference.prediction.fields["document_type"].value
        is None
    )

    assert isinstance(
        international_id_v1_empty_doc.inference.prediction.fields["document_number"],
        StringField,
    )
    assert (
        international_id_v1_empty_doc.inference.prediction.fields[
            "document_number"
        ].value
        is None
    )

    assert isinstance(
        international_id_v1_empty_doc.inference.prediction.fields["country_of_issue"],
        StringField,
    )
    assert (
        international_id_v1_empty_doc.inference.prediction.fields[
            "country_of_issue"
        ].value
        is None
    )

    assert isinstance(
        international_id_v1_empty_doc.inference.prediction.fields["surnames"],
        GeneratedListField,
    )
    assert (
        len(
            international_id_v1_empty_doc.inference.prediction.fields["surnames"].values
        )
        == 0
    )

    assert isinstance(
        international_id_v1_empty_doc.inference.prediction.fields["given_names"],
        GeneratedListField,
    )
    assert (
        len(
            international_id_v1_empty_doc.inference.prediction.fields[
                "given_names"
            ].values
        )
        == 0
    )

    assert isinstance(
        international_id_v1_empty_doc.inference.prediction.fields["sex"],
        StringField,
    )
    assert (
        international_id_v1_empty_doc.inference.prediction.fields["sex"].value is None
    )

    assert isinstance(
        international_id_v1_empty_doc.inference.prediction.fields["birth_date"],
        StringField,
    )
    assert (
        international_id_v1_empty_doc.inference.prediction.fields["birth_date"].value
        is None
    )

    assert isinstance(
        international_id_v1_empty_doc.inference.prediction.fields["birth_place"],
        StringField,
    )
    assert (
        international_id_v1_empty_doc.inference.prediction.fields["birth_place"].value
        is None
    )

    assert isinstance(
        international_id_v1_empty_doc.inference.prediction.fields["nationality"],
        StringField,
    )
    assert (
        international_id_v1_empty_doc.inference.prediction.fields["nationality"].value
        is None
    )

    assert isinstance(
        international_id_v1_empty_doc.inference.prediction.fields["issue_date"],
        StringField,
    )
    assert (
        international_id_v1_empty_doc.inference.prediction.fields["issue_date"].value
        is None
    )

    assert isinstance(
        international_id_v1_empty_doc.inference.prediction.fields["expiry_date"],
        StringField,
    )
    assert (
        international_id_v1_empty_doc.inference.prediction.fields["expiry_date"].value
        is None
    )

    assert isinstance(
        international_id_v1_empty_doc.inference.prediction.fields["address"],
        StringField,
    )
    assert (
        international_id_v1_empty_doc.inference.prediction.fields["address"].value
        is None
    )

    assert isinstance(
        international_id_v1_empty_doc.inference.prediction.fields["mrz1"],
        StringField,
    )
    assert (
        international_id_v1_empty_doc.inference.prediction.fields["mrz1"].value is None
    )
    assert isinstance(
        international_id_v1_empty_doc.inference.prediction.fields["mrz2"],
        StringField,
    )
    assert (
        international_id_v1_empty_doc.inference.prediction.fields["mrz2"].value is None
    )
    assert isinstance(
        international_id_v1_empty_doc.inference.prediction.fields["mrz3"],
        StringField,
    )
    assert (
        international_id_v1_empty_doc.inference.prediction.fields["mrz3"].value is None
    )
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
        international_id_v1_complete_doc.inference.prediction.fields["document_type"],
        StringField,
    )
    assert (
        international_id_v1_complete_doc.inference.prediction.fields[
            "document_type"
        ].value
        == "NATIONAL_ID_CARD"
    )

    assert isinstance(
        international_id_v1_complete_doc.inference.prediction.fields["document_number"],
        StringField,
    )
    assert (
        international_id_v1_complete_doc.inference.prediction.fields[
            "document_number"
        ].value
        == "99999999R"
    )

    assert isinstance(
        international_id_v1_complete_doc.inference.prediction.fields[
            "country_of_issue"
        ],
        StringField,
    )
    assert (
        international_id_v1_complete_doc.inference.prediction.fields[
            "country_of_issue"
        ].value
        == "ESP"
    )

    assert isinstance(
        international_id_v1_complete_doc.inference.prediction.fields["surnames"],
        GeneratedListField,
    )
    assert (
        international_id_v1_complete_doc.inference.prediction.fields["surnames"]
        .values[0]
        .value
        == "ESPAÑOLA"
    )
    assert (
        international_id_v1_complete_doc.inference.prediction.fields["surnames"]
        .values[1]
        .value
        == "ESPAÑOLA"
    )

    assert isinstance(
        international_id_v1_complete_doc.inference.prediction.fields["given_names"],
        GeneratedListField,
    )
    assert (
        international_id_v1_complete_doc.inference.prediction.fields["given_names"]
        .values[0]
        .value
        == "CARMEN"
    )

    assert isinstance(
        international_id_v1_complete_doc.inference.prediction.fields["sex"],
        StringField,
    )
    assert (
        international_id_v1_complete_doc.inference.prediction.fields["sex"].value == "F"
    )

    assert isinstance(
        international_id_v1_complete_doc.inference.prediction.fields["birth_date"],
        StringField,
    )
    assert (
        international_id_v1_complete_doc.inference.prediction.fields["birth_date"].value
        == "1980-01-01"
    )

    assert isinstance(
        international_id_v1_complete_doc.inference.prediction.fields["birth_place"],
        StringField,
    )
    assert (
        international_id_v1_complete_doc.inference.prediction.fields[
            "birth_place"
        ].value
        == "MADRID"
    )

    assert isinstance(
        international_id_v1_complete_doc.inference.prediction.fields["nationality"],
        StringField,
    )
    assert (
        international_id_v1_complete_doc.inference.prediction.fields[
            "nationality"
        ].value
        == "ESP"
    )

    assert isinstance(
        international_id_v1_complete_doc.inference.prediction.fields["issue_date"],
        StringField,
    )
    assert (
        international_id_v1_complete_doc.inference.prediction.fields["issue_date"].value
        == "2015-01-01"
    )

    assert isinstance(
        international_id_v1_complete_doc.inference.prediction.fields["expiry_date"],
        StringField,
    )
    assert (
        international_id_v1_complete_doc.inference.prediction.fields[
            "expiry_date"
        ].value
        == "2025-01-01"
    )

    assert isinstance(
        international_id_v1_complete_doc.inference.prediction.fields["address"],
        StringField,
    )
    assert (
        international_id_v1_complete_doc.inference.prediction.fields["address"].value
        == "AVDA DE MADRID S-N MADRID MADRID"
    )

    assert isinstance(
        international_id_v1_complete_doc.inference.prediction.fields["mrz1"],
        StringField,
    )
    assert (
        international_id_v1_complete_doc.inference.prediction.fields["mrz1"].value
        == "IDESPBAA000589599999999R<<<<<<"
    )
    assert isinstance(
        international_id_v1_complete_doc.inference.prediction.fields["mrz2"],
        StringField,
    )
    assert (
        international_id_v1_complete_doc.inference.prediction.fields["mrz2"].value
        == "8001014F2501017ESP<<<<<<<<<<<7"
    )
    assert isinstance(
        international_id_v1_complete_doc.inference.prediction.fields["mrz3"],
        StringField,
    )
    assert (
        international_id_v1_complete_doc.inference.prediction.fields["mrz3"].value
        == "ESPANOLA<ESPANOLA<<CARMEN<<<<<<"
    )

    assert str(international_id_v1_complete_doc) == doc_str


def test_invoice_v4_complete_doc(invoice_v4_complete_doc) -> None:
    doc_str = open(
        PRODUCT_DATA_DIR / "generated" / "response_v1" / "summary_full_invoice_v4.rst",
        encoding="utf-8",
    ).read()
    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields["customer_address"],
        StringField,
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["customer_address"].value
        == "1954 Bloon Street West Toronto, ON, M6P 3K9 Canada"
    )
    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields[
            "customer_company_registrations"
        ],
        GeneratedListField,
    )
    assert (
        len(
            invoice_v4_complete_doc.inference.prediction.fields[
                "customer_company_registrations"
            ].values
        )
        == 0
    )

    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields["customer_name"],
        StringField,
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["customer_name"].value
        == "JIRO DOI"
    )

    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields["date"],
        StringField,
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["date"].value
        == "2020-02-17"
    )

    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields["document_type"],
        StringField,
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["document_type"].value
        == "INVOICE"
    )

    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields["due_date"],
        StringField,
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["due_date"].value
        == "2020-02-17"
    )

    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields["invoice_number"],
        StringField,
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["invoice_number"].value
        == "0042004801351"
    )

    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields["line_items"],
        GeneratedListField,
    )
    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields["line_items"].values[0],
        GeneratedObjectField,
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["line_items"]
        .values[0]
        .description
        == "S)BOIE 5X500 FEUILLES A4"
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["line_items"]
        .values[0]
        .product_code
        is None
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["line_items"]
        .values[0]
        .quantity
        is None
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["line_items"]
        .values[6]
        .quantity
        == "1.0"
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["line_items"]
        .values[0]
        .tax_amount
        is None
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["line_items"]
        .values[0]
        .tax_rate
        is None
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["line_items"]
        .values[0]
        .total_amount
        == "2.63"
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["line_items"]
        .values[0]
        .unit_price
        is None
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["line_items"]
        .values[6]
        .unit_price
        == "65.0"
    )

    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields["locale"],
        GeneratedObjectField,
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["locale"].currency == "EUR"
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["locale"].language == "fr"
    )

    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields["reference_numbers"],
        GeneratedListField,
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["reference_numbers"]
        .values[0]
        .value
        == "AD29094"
    )

    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields["supplier_address"],
        StringField,
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["supplier_address"].value
        == "156 University Ave, Toronto ON, Canada M5H 2H7"
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

    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields["supplier_name"],
        StringField,
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["supplier_name"].value
        == "TURNPIKE DESIGNS CO."
    )

    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields["supplier_payment_details"],
        GeneratedListField,
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["supplier_payment_details"]
        .values[0]
        .iban
        == "FR7640254025476501124705368"
    )

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
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["taxes"].values[0].rate
        == "20.0"
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["taxes"].values[0].value
        == "97.98"
    )

    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields["total_amount"], StringField
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["total_amount"].value
        == "587.95"
    )

    assert isinstance(
        invoice_v4_complete_doc.inference.prediction.fields["total_net"], StringField
    )
    assert (
        invoice_v4_complete_doc.inference.prediction.fields["total_net"].value
        == "489.97"
    )

    assert str(invoice_v4_complete_doc) == doc_str


def test_invoice_v4_page0(invoice_v4_page_0) -> None:
    doc_str = open(
        PRODUCT_DATA_DIR / "generated" / "response_v1" / "summary_page0_invoice_v4.rst",
        encoding="utf-8",
    ).read()

    assert isinstance(
        invoice_v4_page_0.prediction.fields["customer_address"],
        StringField,
    )
    assert invoice_v4_page_0.prediction.fields["customer_address"].value is None
    assert isinstance(
        invoice_v4_page_0.prediction.fields["customer_company_registrations"],
        GeneratedListField,
    )
    assert (
        len(
            invoice_v4_page_0.prediction.fields["customer_company_registrations"].values
        )
        == 0
    )

    assert isinstance(
        invoice_v4_page_0.prediction.fields["customer_name"],
        StringField,
    )
    assert invoice_v4_page_0.prediction.fields["customer_name"].value is None

    assert isinstance(
        invoice_v4_page_0.prediction.fields["date"],
        StringField,
    )
    assert invoice_v4_page_0.prediction.fields["date"].value == "2020-02-17"

    assert isinstance(
        invoice_v4_page_0.prediction.fields["document_type"],
        StringField,
    )
    assert invoice_v4_page_0.prediction.fields["document_type"].value == "INVOICE"

    assert isinstance(
        invoice_v4_page_0.prediction.fields["due_date"],
        StringField,
    )
    assert invoice_v4_page_0.prediction.fields["due_date"].value == "2020-02-17"

    assert isinstance(
        invoice_v4_page_0.prediction.fields["invoice_number"],
        StringField,
    )
    assert (
        invoice_v4_page_0.prediction.fields["invoice_number"].value == "0042004801351"
    )

    assert isinstance(
        invoice_v4_page_0.prediction.fields["line_items"],
        GeneratedListField,
    )
    assert isinstance(
        invoice_v4_page_0.prediction.fields["line_items"].values[0],
        GeneratedObjectField,
    )
    assert (
        invoice_v4_page_0.prediction.fields["line_items"].values[0].description
        == "S)BOIE 5X500 FEUILLES A4"
    )
    assert (
        invoice_v4_page_0.prediction.fields["line_items"].values[0].product_code is None
    )
    assert invoice_v4_page_0.prediction.fields["line_items"].values[0].quantity is None
    assert (
        invoice_v4_page_0.prediction.fields["line_items"].values[0].tax_amount is None
    )
    assert invoice_v4_page_0.prediction.fields["line_items"].values[0].tax_rate is None
    assert (
        invoice_v4_page_0.prediction.fields["line_items"].values[0].total_amount
        == "2.63"
    )
    assert (
        invoice_v4_page_0.prediction.fields["line_items"].values[0].unit_price is None
    )

    assert isinstance(
        invoice_v4_page_0.prediction.fields["locale"],
        GeneratedObjectField,
    )
    assert invoice_v4_page_0.prediction.fields["locale"].currency == "EUR"
    assert invoice_v4_page_0.prediction.fields["locale"].language == "fr"

    assert isinstance(
        invoice_v4_page_0.prediction.fields["reference_numbers"],
        GeneratedListField,
    )
    assert len(invoice_v4_page_0.prediction.fields["reference_numbers"].values) == 0

    assert isinstance(
        invoice_v4_page_0.prediction.fields["supplier_address"],
        StringField,
    )
    assert invoice_v4_page_0.prediction.fields["supplier_address"].value is None
    assert isinstance(
        invoice_v4_page_0.prediction.fields["supplier_company_registrations"],
        GeneratedListField,
    )
    assert (
        len(
            invoice_v4_page_0.prediction.fields["supplier_company_registrations"].values
        )
        == 0
    )

    assert isinstance(
        invoice_v4_page_0.prediction.fields["supplier_name"],
        StringField,
    )
    assert invoice_v4_page_0.prediction.fields["supplier_name"].value is None

    assert isinstance(
        invoice_v4_page_0.prediction.fields["supplier_payment_details"],
        GeneratedListField,
    )
    assert (
        invoice_v4_page_0.prediction.fields["supplier_payment_details"].values[0].iban
        == "FR7640254025476501124705368"
    )

    assert isinstance(invoice_v4_page_0.prediction.fields["taxes"], GeneratedListField)
    assert isinstance(
        invoice_v4_page_0.prediction.fields["taxes"].values[0].polygon,
        PositionField,
    )
    assert [
        [point.x, point.y]
        for point in invoice_v4_page_0.prediction.fields["taxes"]
        .values[0]
        .polygon.value
    ] == [[0.292, 0.749], [0.543, 0.749], [0.543, 0.763], [0.292, 0.763]]
    assert invoice_v4_page_0.prediction.fields["taxes"].values[0].rate == "20.0"
    assert invoice_v4_page_0.prediction.fields["taxes"].values[0].value == "97.98"

    assert isinstance(invoice_v4_page_0.prediction.fields["total_amount"], StringField)
    assert invoice_v4_page_0.prediction.fields["total_amount"].value == "587.95"

    assert isinstance(invoice_v4_page_0.prediction.fields["total_net"], StringField)
    assert invoice_v4_page_0.prediction.fields["total_net"].value == "489.97"
    assert str(invoice_v4_page_0) == doc_str


def test_invoice_v4_empty_doc(invoice_v4_empty_doc) -> None:
    doc_str = open(
        PRODUCT_DATA_DIR / "generated" / "response_v1" / "summary_empty_invoice_v4.rst",
        encoding="utf-8",
    ).read()

    assert isinstance(
        invoice_v4_empty_doc.inference.prediction.fields["customer_address"],
        StringField,
    )
    assert (
        invoice_v4_empty_doc.inference.prediction.fields["customer_address"].value
        is None
    )
    assert isinstance(
        invoice_v4_empty_doc.inference.prediction.fields[
            "customer_company_registrations"
        ],
        GeneratedListField,
    )
    assert (
        len(
            invoice_v4_empty_doc.inference.prediction.fields[
                "customer_company_registrations"
            ].values
        )
        == 0
    )

    assert isinstance(
        invoice_v4_empty_doc.inference.prediction.fields["customer_name"],
        StringField,
    )
    assert (
        invoice_v4_empty_doc.inference.prediction.fields["customer_name"].value is None
    )

    assert isinstance(
        invoice_v4_empty_doc.inference.prediction.fields["date"],
        StringField,
    )
    assert invoice_v4_empty_doc.inference.prediction.fields["date"].value is None

    assert isinstance(
        invoice_v4_empty_doc.inference.prediction.fields["document_type"],
        StringField,
    )
    assert (
        invoice_v4_empty_doc.inference.prediction.fields["document_type"].value
        == "INVOICE"
    )

    assert isinstance(
        invoice_v4_empty_doc.inference.prediction.fields["due_date"],
        StringField,
    )
    assert invoice_v4_empty_doc.inference.prediction.fields["due_date"].value is None

    assert isinstance(
        invoice_v4_empty_doc.inference.prediction.fields["invoice_number"],
        StringField,
    )
    assert (
        invoice_v4_empty_doc.inference.prediction.fields["invoice_number"].value is None
    )

    assert isinstance(
        invoice_v4_empty_doc.inference.prediction.fields["line_items"],
        GeneratedListField,
    )
    assert (
        len(invoice_v4_empty_doc.inference.prediction.fields["line_items"].values) == 0
    )

    assert isinstance(
        invoice_v4_empty_doc.inference.prediction.fields["locale"],
        GeneratedObjectField,
    )
    assert invoice_v4_empty_doc.inference.prediction.fields["locale"].currency is None
    assert invoice_v4_empty_doc.inference.prediction.fields["locale"].language is None

    assert isinstance(
        invoice_v4_empty_doc.inference.prediction.fields["reference_numbers"],
        GeneratedListField,
    )
    assert (
        len(
            invoice_v4_empty_doc.inference.prediction.fields["reference_numbers"].values
        )
        == 0
    )

    assert isinstance(
        invoice_v4_empty_doc.inference.prediction.fields["supplier_address"],
        StringField,
    )
    assert (
        invoice_v4_empty_doc.inference.prediction.fields["supplier_address"].value
        is None
    )
    assert isinstance(
        invoice_v4_empty_doc.inference.prediction.fields[
            "supplier_company_registrations"
        ],
        GeneratedListField,
    )
    assert (
        len(
            invoice_v4_empty_doc.inference.prediction.fields[
                "supplier_company_registrations"
            ].values
        )
        == 0
    )

    assert isinstance(
        invoice_v4_empty_doc.inference.prediction.fields["supplier_name"],
        StringField,
    )
    assert (
        invoice_v4_empty_doc.inference.prediction.fields["supplier_name"].value is None
    )

    assert isinstance(
        invoice_v4_empty_doc.inference.prediction.fields["supplier_payment_details"],
        GeneratedListField,
    )
    assert (
        len(
            invoice_v4_empty_doc.inference.prediction.fields[
                "supplier_payment_details"
            ].values
        )
        == 0
    )

    assert isinstance(
        invoice_v4_empty_doc.inference.prediction.fields["taxes"], GeneratedListField
    )
    assert len(invoice_v4_empty_doc.inference.prediction.fields["taxes"].values) == 0

    assert isinstance(
        invoice_v4_empty_doc.inference.prediction.fields["total_amount"], StringField
    )
    assert (
        invoice_v4_empty_doc.inference.prediction.fields["total_amount"].value is None
    )

    assert isinstance(
        invoice_v4_empty_doc.inference.prediction.fields["total_net"], StringField
    )
    assert invoice_v4_empty_doc.inference.prediction.fields["total_net"].value is None

    assert str(invoice_v4_empty_doc) == doc_str
