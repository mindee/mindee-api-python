import json
import pytest
from mindee import FinancialDocument


@pytest.fixture
def financial_doc_from_invoice_object():
    invoice_json_repsonse = json.load(open("./tests/data/invoices/v2/invoice.json"))
    return FinancialDocument(invoice_json_repsonse["predictions"][0])


@pytest.fixture
def financial_doc_from_receipt_object():
    receipt_json_repsonse = json.load(open("./tests/data/expense_receipts/v3/receipt.json"))
    return FinancialDocument(receipt_json_repsonse["predictions"][0])


@pytest.fixture
def financial_doc_object_from_scratch():
    return FinancialDocument(
        locale="fr",
        total_incl=12,
        total_excl=15,
        date="2018-12-21",
        invoice_number="001",
        due_date="2019-01-01",
        taxes={(1, 10), (2, 20)},
        merchant_name="Amazon",
        payment_details="1231456498799765",
        company_number="asdqsdae",
        orientation=0,
        total_tax=3,
        time="12:15"
    )


@pytest.fixture
def financial_doc_from_receipt_object_all_na():
    json_repsonse = json.load(open("./tests/data/expense_receipts/v3/receipt_all_na.json"))
    return FinancialDocument(json_repsonse["predictions"][0])


@pytest.fixture
def financial_doc_from_invoice_object_all_na():
    json_repsonse = json.load(open("./tests/data/invoices/v2/invoice_all_na.json"))
    return FinancialDocument(json_repsonse["predictions"][0])


@pytest.fixture
def receipt_pred():
    return json.load(open("./tests/data/expense_receipts/v3/receipt_all_na.json"))["predictions"][0]


@pytest.fixture
def invoice_pred():
    return json.load(open("./tests/data/invoices/v2/invoice_all_na.json"))["predictions"][0]


def test_constructor_1(financial_doc_from_invoice_object):
    assert financial_doc_from_invoice_object.date.value == "2020-02-17"


def test_constructor_2(financial_doc_from_receipt_object):
    assert financial_doc_from_receipt_object.date.value == "2016-02-26"


def test_all_na_receipt(financial_doc_from_receipt_object_all_na):
    assert financial_doc_from_receipt_object_all_na.orientation.value == 0
    assert financial_doc_from_receipt_object_all_na.locale.value is None
    assert financial_doc_from_receipt_object_all_na.total_incl.value is None
    assert financial_doc_from_receipt_object_all_na.date.value is None
    assert financial_doc_from_receipt_object_all_na.merchant_name.value is None
    assert financial_doc_from_receipt_object_all_na.total_tax.value is None
    assert len(financial_doc_from_receipt_object_all_na.taxes) == 0


def test_all_na_invoice(financial_doc_from_invoice_object_all_na):
    assert financial_doc_from_invoice_object_all_na.orientation.value == 0
    assert financial_doc_from_invoice_object_all_na.locale.value is None
    assert financial_doc_from_invoice_object_all_na.total_incl.value is None
    assert financial_doc_from_invoice_object_all_na.date.value is None
    assert financial_doc_from_invoice_object_all_na.merchant_name.value is None
    assert financial_doc_from_invoice_object_all_na.total_tax.value is None
    assert len(financial_doc_from_invoice_object_all_na.taxes) == 0


def test__str__invoice(financial_doc_from_invoice_object):
    assert type(financial_doc_from_invoice_object.__str__()) == str


def test__str__receipt(financial_doc_from_receipt_object):
    assert type(financial_doc_from_receipt_object.__str__()) == str


# Business tests from receipt
def test__receipt_reconstruct_total_excl_from_total_and_taxes_1(receipt_pred):
    # no incl implies no reconstruct for total excl
    receipt_pred["total_incl"] = {"value": "N/A", "probability": 0.}
    receipt_pred["taxes"] = [{"rate": 20, "value": 9.5, "probability": 0.9}]
    financial_doc = FinancialDocument(receipt_pred)
    assert financial_doc.total_excl.value is None


def test__receipt_reconstruct_total_excl_from_total_and_taxes_2(receipt_pred):
    # no taxes implies no reconstruct for total excl
    receipt_pred["total_incl"] = {"value": 12.54, "probability": 0.}
    receipt_pred["taxes"] = []
    financial_doc = FinancialDocument(receipt_pred)
    assert financial_doc.total_excl.value is None


def test__receipt_reconstruct_total_excl_from_total_and_taxes_3(receipt_pred):
    # working example
    receipt_pred["total_incl"] = {"value": 12.54, "probability": 0.5}
    receipt_pred["taxes"] = [{"rate": 20, "value": 0.5, "probability": 0.1},
                             {"rate": 10, "value": 4.25, "probability": 0.6}]
    financial_doc = FinancialDocument(receipt_pred)
    assert financial_doc.total_excl.probability == 0.03
    assert financial_doc.total_excl.value == 7.79


def test__receipt_reconstruct_total_tax_1(receipt_pred):
    # no taxes implies no reconstruct for total tax
    receipt_pred["taxes"] = []
    financial_doc = FinancialDocument(receipt_pred)
    assert financial_doc.total_tax.value is None


def test__receipt_reconstruct_total_tax_2(receipt_pred):
    # working example
    receipt_pred["taxes"] = [{"rate": 20, "value": 10.2, "probability": 0.5},
                             {"rate": 10, "value": 40.0, "probability": 0.1}]
    financial_doc = FinancialDocument(receipt_pred)
    assert financial_doc.total_tax.value == 50.2
    assert financial_doc.total_tax.probability == 0.05


def test__receipt_taxes_match_total_incl_1(receipt_pred):
    # matching example
    receipt_pred["total_incl"] = {"value": 507.25, "probability": 0.6}
    receipt_pred["taxes"] = [{"rate": 20, "value": 10.99, "probability": 0.5},
                             {"rate": 10, "value": 40.12, "probability": 0.1}]
    financial_doc = FinancialDocument(receipt_pred)
    assert financial_doc.checklist["taxes_match_total_incl"] is True
    assert financial_doc.total_incl.probability == 1.
    for tax in financial_doc.taxes:
        assert tax.probability == 1.


def test__receipt_taxes_match_total_incl_2(receipt_pred):
    # not matching example with close error
    receipt_pred["total_incl"] = {"value": 507.25, "probability": 0.6}
    receipt_pred["taxes"] = [{"rate": 20, "value": 10.9, "probability": 0.5},
                             {"rate": 10, "value": 40.12, "probability": 0.1}]
    financial_doc = FinancialDocument(receipt_pred)
    assert financial_doc.checklist["taxes_match_total_incl"] is False


def test__receipt_taxes_match_total_incl_3(receipt_pred):
    # sanity check with null tax
    receipt_pred["total_incl"] = {"value": 507.25, "probability": 0.6}
    receipt_pred["taxes"] = [{"rate": 20, "value": 0., "probability": 0.5}]
    financial_doc = FinancialDocument(receipt_pred)
    assert financial_doc.checklist["taxes_match_total_incl"] is False


# Business tests from invoice
def test__invoice_reconstruct_total_excl_from_total_and_taxes_1(invoice_pred):
    # no incl implies no reconstruct for total excl
    invoice_pred["total_incl"] = {"amount": "N/A", "probability": 0.}
    invoice_pred["taxes"] = [{"rate": 20, "amount": 9.5, "probability": 0.9}]
    financial_doc = FinancialDocument(invoice_pred)
    assert financial_doc.total_excl.value is None


def test__invoice_reconstruct_total_excl_from_total_and_taxes_2(invoice_pred):
    # no taxes implies no reconstruct for total excl
    invoice_pred["total_incl"] = {"amount": 12.54, "probability": 0.}
    invoice_pred["taxes"] = []
    financial_doc = FinancialDocument(invoice_pred)
    assert financial_doc.total_excl.value is None


def test__invoice_reconstruct_total_excl_from_total_and_taxes_3(invoice_pred):
    # working example
    invoice_pred["total_incl"] = {"value": 12.54, "probability": 0.5}
    invoice_pred["taxes"] = [{"rate": 20, "value": 0.5, "probability": 0.1},
                             {"rate": 10, "value": 4.25, "probability": 0.6}]
    financial_doc = FinancialDocument(invoice_pred)
    assert financial_doc.total_excl.probability == 0.03
    assert financial_doc.total_excl.value == 7.79


def test__invoice_reconstruct_total_tax_1(invoice_pred):
    # no taxes implies no reconstruct for total tax
    invoice_pred["taxes"] = []
    financial_doc = FinancialDocument(invoice_pred)
    assert financial_doc.total_tax.value is None


def test__invoice_reconstruct_total_tax_2(invoice_pred):
    # working example
    invoice_pred["taxes"] = [{"rate": 20, "value": 10.2, "probability": 0.5},
                             {"rate": 10, "value": 40.0, "probability": 0.1}]
    financial_doc = FinancialDocument(invoice_pred)
    assert financial_doc.total_tax.value == 50.2
    assert financial_doc.total_tax.probability == 0.05


def test__invoice_taxes_match_total_incl_1(invoice_pred):
    # matching example
    invoice_pred["total_incl"] = {"value": 507.25, "probability": 0.6}
    invoice_pred["taxes"] = [{"rate": 20, "value": 10.99, "probability": 0.5},
                             {"rate": 10, "value": 40.12, "probability": 0.1}]
    financial_doc = FinancialDocument(invoice_pred)
    assert financial_doc.checklist["taxes_match_total_incl"] is True
    assert financial_doc.total_incl.probability == 1.
    for tax in financial_doc.taxes:
        assert tax.probability == 1.


def test__invoice_taxes_match_total_incl_2(invoice_pred):
    # not matching example with close error
    invoice_pred["total_incl"] = {"value": 507.25, "probability": 0.6}
    invoice_pred["taxes"] = [{"rate": 20, "value": 10.9, "probability": 0.5},
                             {"rate": 10, "value": 40.12, "probability": 0.1}]
    financial_doc = FinancialDocument(invoice_pred)
    assert financial_doc.checklist["taxes_match_total_incl"] is False


def test__invoice_taxes_match_total_incl_3(invoice_pred):
    # sanity check with null tax
    invoice_pred["total_incl"] = {"value": 507.25, "probability": 0.6}
    invoice_pred["taxes"] = [{"rate": 20, "value": 0., "probability": 0.5}]
    financial_doc = FinancialDocument(invoice_pred)
    assert financial_doc.checklist["taxes_match_total_incl"] is False


def test__shouldnt_raise_when_tax_rate_none(invoice_pred):
    # sanity check with null tax
    invoice_pred["total_incl"] = {"value": 507.25, "probability": 0.6}
    invoice_pred["taxes"] = [{"rate": "N/A", "value": 0., "probability": 0.5}]
    financial_doc = FinancialDocument(invoice_pred)
    assert financial_doc.checklist["taxes_match_total_incl"] is False


def test_compare_1(financial_doc_from_invoice_object):
    # Compare same object must return all True
    benchmark = FinancialDocument.compare(financial_doc_from_invoice_object, financial_doc_from_invoice_object)
    for value in benchmark.values():
        assert value is True


def test_compare_2(financial_doc_from_invoice_object, financial_doc_from_invoice_object_all_na):
    # Compare full object and empty object
    benchmark = FinancialDocument.compare(financial_doc_from_invoice_object, financial_doc_from_invoice_object_all_na)
    for key in set(benchmark.keys()) - {"time"}:
        assert benchmark[key] is False


def test_compare_3(financial_doc_object_from_scratch):
    # Compare financial doc from class
    benchmark = FinancialDocument.compare(
        financial_doc_object_from_scratch,
        financial_doc_object_from_scratch
    )
    for key in benchmark.keys():
        if "__acc__" in key:
            assert benchmark[key] is True


def test_compare_4(financial_doc_object_from_scratch):
    # Compare financial doc from class with empty taxes
    financial_doc_object_from_scratch.taxes = []
    benchmark = FinancialDocument.compare(
        financial_doc_object_from_scratch,
        financial_doc_object_from_scratch
    )
    for key in benchmark.keys():
        if "__acc__" in key:
            assert benchmark[key] is True
        elif "__pre__" in key:
            assert benchmark[key] in [True, None]


def test_empty_object_works():
    financial_doc = FinancialDocument()
    assert financial_doc.total_tax.value is None
