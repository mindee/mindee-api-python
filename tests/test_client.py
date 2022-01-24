import io
import pytest
from mindee import Client, Response
from mindee.http import HTTPException


@pytest.fixture
def empty_client():
    return Client()


@pytest.fixture
def env_client(monkeypatch):
    monkeypatch.setenv("MINDEE_RECEIPT_API_KEY", "dummy")
    monkeypatch.setenv("MINDEE_INVOICE_API_KEY", "dummy")
    monkeypatch.setenv("MINDEE_PASSPORT_API_KEY", "dummy")
    return Client()


@pytest.fixture
def dummy_client():
    return Client(
        receipt_api_key="dummy",
        invoice_api_key="dummy",
        passport_api_key="dummy",
    )


@pytest.fixture
def dummy_client_no_raise():
    return Client(
        receipt_api_key="dummy",
        invoice_api_key="dummy",
        passport_api_key="dummy",
        raise_on_error=False,
    )


@pytest.fixture
def response():
    return Response.load("./tests/data/expense_receipts/v3/receipt.json")


def test_parse_path_without_token(empty_client):
    with pytest.raises(AssertionError):
        empty_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpg", document_type="receipt"
        )
    with pytest.raises(AssertionError):
        empty_client.parse_from_path(
            "./tests/data/invoices/invoice.pdf", document_type="invoice"
        )
    with pytest.raises(AssertionError):
        empty_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpg",
            document_type="financial_document",
        )
    with pytest.raises(AssertionError):
        empty_client.parse_from_path(
            "./tests/data/passport/passport.jpeg", document_type="passport"
        )


def test_parse_path_with_env_token(env_client):
    with pytest.raises(HTTPException):
        env_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpg", document_type="receipt"
        )
    with pytest.raises(HTTPException):
        env_client.parse_from_path(
            "./tests/data/invoices/invoice.pdf", document_type="invoice"
        )
    with pytest.raises(HTTPException):
        env_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpg",
            document_type="financial_document",
        )
    with pytest.raises(HTTPException):
        env_client.parse_from_path(
            "./tests/data/passport/passport.jpeg", document_type="passport"
        )


def test_parse_path_with_wrong_filetype(dummy_client):
    with pytest.raises(AssertionError):
        dummy_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpga", document_type="receipt"
        )
    with pytest.raises(AssertionError):
        dummy_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpga", document_type="invoice"
        )
    with pytest.raises(AssertionError):
        dummy_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpga",
            document_type="financial_document",
        )
    with pytest.raises(AssertionError):
        dummy_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpga", document_type="passport"
        )


def test_parse_path_with_wrong_token(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpg", document_type="receipt"
        )
    with pytest.raises(HTTPException):
        dummy_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpg", document_type="invoice"
        )
    with pytest.raises(HTTPException):
        dummy_client.parse_from_path(
            "./tests/data/expense_receipts/receipt.jpg",
            document_type="financial_document",
        )
    with pytest.raises(HTTPException):
        dummy_client.parse_from_path(
            "./tests/data/invoices/invoice.pdf", document_type="financial_document"
        )
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
            "./tests/data/expense_receipts/receipt.jpg", document_type="receipt"
        )


def test_request_with_base64_no_filename(dummy_client):
    with open("./tests/data/expense_receipts/receipt.txt", "r") as fh:
        b64 = fh.read()
    with pytest.raises(TypeError):
        dummy_client.parse_from_b64string(b64, document_type="receipt")


def test_request_without_raise_on_error(dummy_client_no_raise):
    result = dummy_client_no_raise.parse_from_path(
        "./tests/data/expense_receipts/receipt.jpg", "receipt"
    )
    assert result.receipt is None
    assert len(result.receipts) == 0


def test_request_without_raise_on_error_include_words(dummy_client_no_raise):
    result = dummy_client_no_raise.parse_from_path(
        "./tests/data/expense_receipts/receipt.jpg",
        include_words=True,
        document_type="receipt",
    )
    assert result.receipt is None
    assert len(result.receipts) == 0


def test_request_with_wrong_type(dummy_client):
    with pytest.raises(TypeError):
        dummy_client.parse_from_path(
            open("./tests/data/test.txt"), document_type="receipt"
        )
    with pytest.raises(AttributeError):
        dummy_client.parse_from_file("./tests/data/test.txt", document_type="receipt")
    with pytest.raises(TypeError):
        dummy_client.parse_from_b64string(
            open("./tests/data/test.txt"), "test.jpg", document_type="receipt"
        )


def test_pdf_reconstruct(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.parse_from_path(
            "./tests/data/invoices/invoice_6p.pdf", document_type="invoice"
        )
