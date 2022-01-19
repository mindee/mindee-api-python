import pytest
from mindee import Client, Response, Receipt, Passport
from mindee.http import HTTPException


@pytest.fixture
def empty_client():
    return Client()


@pytest.fixture
def dummy_client():
    return Client(
        receipt_api_key="dummy",
        invoice_api_key="dummy",
        passport_api_key="dummy",
    )


@pytest.fixture
def dummy_client_dont_raise():
    return Client(
        receipt_api_key="dummy",
        invoice_api_key="dummy",
        passport_api_key="dummy",
        raise_on_error=False,
    )


@pytest.fixture
def response():
    return Response.load("./tests/data/expense_receipts/v3/receipt.json")


def test_parse_receipt_without_token(empty_client):
    with pytest.raises(AssertionError):
        empty_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpg", document_type="receipt"
        )


def test_parse_invoice_without_token(empty_client):
    with pytest.raises(AssertionError):
        empty_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpg", document_type="invoice"
        )


def test_parse_financial_doc_without_token(empty_client):
    with pytest.raises(AssertionError):
        empty_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpg",
            document_type="financial_document",
        )


def test_parse_passport_without_token(empty_client):
    with pytest.raises(AssertionError):
        empty_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpg", document_type="passport"
        )


def test_parse_receipt_with_wrong_filetype(dummy_client):
    with pytest.raises(AssertionError):
        dummy_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpga", document_type="receipt"
        )


def test_parse_invoice_with_wrong_filetype(dummy_client):
    with pytest.raises(AssertionError):
        dummy_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpga", document_type="invoice"
        )


def test_parse_financial_doc_with_wrong_filetype(dummy_client):
    with pytest.raises(AssertionError):
        dummy_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpga",
            document_type="financial_document",
        )


def test_parse_passport_with_wrong_filetype(dummy_client):
    with pytest.raises(AssertionError):
        dummy_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpga", document_type="passport"
        )


def test_parse_receipt_with_wrong_token(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpg", document_type="receipt"
        )


def test_parse_invoice_with_wrong_token(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpg", document_type="invoice"
        )


def test_parse_financial_doc_with_wrong_token_jpg(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpg",
            document_type="financial_document",
        )


def test_parse_financial_doc_with_wrong_token_pdf(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.parse_from_path(
            "./tests/data/invoices/invoice.pdf", document_type="financial_document"
        )


def test_parse_passport_with_wrong_token(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpg", document_type="passport"
        )


def test_response_load_failure():
    with pytest.raises(Exception):
        Response.load("notAFile")


def test_request_with_filepath(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpg",
            document_type="receipt",
        )


# def test_request_with_file(dummy_client):
#     with pytest.raises(AssertionError):
#         dummy_client.parse(
#             open("./tests/data/expense_receipts/receipt.jpg"),
#             input_type="file",
#             document_type="receipt",
#         )


def test_request_with_base64_no_filename(dummy_client):
    with open("./tests/data/expense_receipts/receipt.txt", "r") as fh:
        b64 = fh.read()
    with pytest.raises(TypeError):
        dummy_client.parse_from_string(b64, document_type="receipt")


def test_request_with_base64(dummy_client):
    with open("./tests/data/expense_receipts/receipt.txt", "r") as fh:
        b64 = fh.read()
    with pytest.raises(HTTPException):
        dummy_client.parse_from_string(
            b64, document_type="receipt", filename="receipt.txt"
        )


def test_request_without_raise_on_error(dummy_client_dont_raise):
    result = dummy_client_dont_raise.parse_from_path(
        "./tests/data/expense_receipts/receipt.jpg",
        "receipt",
    )
    assert result.receipt is None
    assert len(result.receipts) == 0


def test_request_without_raise_on_error_include_words(dummy_client_dont_raise):
    result = dummy_client_dont_raise.parse_from_path(
        "./tests/data/expense_receipts/receipt.jpg",
        include_words=True,
        document_type="receipt",
    )
    assert result.receipt is None
    assert len(result.receipts) == 0


def test_request_with_file_wrong_type(dummy_client):
    with pytest.raises(TypeError):
        dummy_client.parse_from_path(
            open("./tests/data/test.txt"), document_type="receipt"
        )
    with pytest.raises(AttributeError):
        dummy_client.parse_from_stream(
            "./tests/data/test.txt", document_type="receipt"
        )
    with pytest.raises(TypeError):
        dummy_client.parse_from_string(
            open("./tests/data/test.txt"), "test.jpg", document_type="receipt"
        )


def test_pdf_reconstruct(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.parse_from_path(
            "./tests/data/invoices/invoice_6p.pdf", document_type="invoice"
        )
