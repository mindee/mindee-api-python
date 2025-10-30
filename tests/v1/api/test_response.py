import json

from mindee.parsing.common.predict_response import PredictResponse
from mindee.product.financial_document.financial_document_v1 import FinancialDocumentV1
from mindee.product.financial_document.financial_document_v1_document import (
    FinancialDocumentV1Document,
)
from mindee.product.fr.id_card.id_card_v2 import IdCardV2
from mindee.product.fr.id_card.id_card_v2_document import IdCardV2Document
from mindee.product.fr.id_card.id_card_v2_page import IdCardV2Page
from mindee.product.invoice.invoice_v4 import InvoiceV4
from mindee.product.invoice.invoice_v4_document import InvoiceV4Document
from mindee.product.passport.passport_v1 import PassportV1
from mindee.product.passport.passport_v1_document import PassportV1Document
from mindee.product.receipt.receipt_v5 import ReceiptV5
from mindee.product.receipt.receipt_v5_document import ReceiptV5Document


def test_invoice_receipt_v5():
    response = json.load(
        open("./tests/data/products/invoices/response_v4/complete.json")
    )
    parsed_response = PredictResponse(InvoiceV4, response)
    assert isinstance(parsed_response.document.inference, InvoiceV4)
    for page in parsed_response.document.inference.pages:
        assert isinstance(page.prediction, InvoiceV4Document)
    assert parsed_response.document.n_pages == 1


def test_response_receipt_v5():
    response = json.load(
        open("./tests/data/products/expense_receipts/response_v5/complete.json")
    )
    parsed_response = PredictResponse(ReceiptV5, response)
    assert isinstance(parsed_response.document.inference, ReceiptV5)
    for page in parsed_response.document.inference.pages:
        assert isinstance(page.prediction, ReceiptV5Document)
    assert parsed_response.document.n_pages == 1


def test_response_financial_doc_with_receipt():
    response = json.load(
        open(
            "./tests/data/products/financial_document/response_v1/complete_receipt.json"
        )
    )
    parsed_response = PredictResponse(FinancialDocumentV1, response)
    assert isinstance(parsed_response.document.inference, FinancialDocumentV1)
    assert isinstance(
        parsed_response.document.inference.prediction, FinancialDocumentV1Document
    )
    for page in parsed_response.document.inference.pages:
        assert isinstance(page.prediction, FinancialDocumentV1Document)


def test_response_passport_v1():
    response = json.load(
        open("./tests/data/products/passport/response_v1/complete.json")
    )
    parsed_response = PredictResponse(PassportV1, response)
    assert isinstance(parsed_response.document.inference, PassportV1)
    assert isinstance(parsed_response.document.inference.prediction, PassportV1Document)
    for page in parsed_response.document.inference.pages:
        assert isinstance(page.prediction, PassportV1Document)
    assert parsed_response.document.n_pages == 1


def test_response_fr_idcard_v2():
    response = json.load(
        open("./tests/data/products/idcard_fr/response_v2/complete.json")
    )
    parsed_response = PredictResponse(IdCardV2, response)
    assert isinstance(parsed_response.document.inference, IdCardV2)
    assert isinstance(parsed_response.document.inference.prediction, IdCardV2Document)
    for page in parsed_response.document.inference.pages:
        assert isinstance(page.prediction, IdCardV2Page)
    assert parsed_response.document.n_pages == 1
