import pytest

from tests.utils import clear_envvars, dummy_envvars

from mindee import Client, DocumentResponse
from mindee.http import HTTPException


@pytest.fixture
def empty_client(monkeypatch):
    clear_envvars(monkeypatch)
    return Client().config_custom_doc(
        document_type="dummy",
        singular_name="dummy",
        plural_name="dummies",
        account_name="dummy",
    )


@pytest.fixture
def env_client(monkeypatch):
    dummy_envvars(monkeypatch)
    return (
        Client()
        .config_receipt()
        .config_invoice()
        .config_passport()
        .config_financial_doc()
        .config_custom_doc(
            document_type="dummy",
            singular_name="dummy",
            plural_name="dummies",
            account_name="dummy",
        )
    )


@pytest.fixture
def dummy_client():
    return (
        Client()
        .config_receipt("dummy")
        .config_invoice("dummy")
        .config_passport("dummy")
        .config_financial_doc("dummy", "dummy")
        .config_custom_doc(
            document_type="dummy",
            singular_name="dummy",
            plural_name="dummies",
            account_name="dummy",
        )
    )


@pytest.fixture
def dummy_client_no_raise():
    return (
        Client(raise_on_error=False)
        .config_receipt("dummy")
        .config_invoice("dummy")
        .config_passport("dummy")
        .config_financial_doc("dummy", "dummy")
    )


@pytest.fixture
def response():
    return DocumentResponse.load("./tests/data/expense_receipts/v3/receipt.json")


def test_parse_path_without_token(empty_client):
    with pytest.raises(RuntimeError):
        empty_client.doc_from_path("./tests/data/expense_receipts/receipt.jpg").parse(
            "receipt"
        )
    with pytest.raises(RuntimeError):
        empty_client.doc_from_path("./tests/data/invoices/invoice.pdf").parse("invoice")
    with pytest.raises(RuntimeError):
        empty_client.doc_from_path("./tests/data/expense_receipts/receipt.jpg").parse(
            "financial_doc"
        )
    with pytest.raises(RuntimeError):
        empty_client.doc_from_path("./tests/data/passport/passport.jpeg").parse(
            "passport"
        )


def test_parse_path_with_env_token(env_client):
    with pytest.raises(HTTPException):
        env_client.doc_from_path("./tests/data/expense_receipts/receipt.jpg").parse(
            "receipt"
        )
    with pytest.raises(HTTPException):
        env_client.doc_from_path("./tests/data/invoices/invoice.pdf").parse("invoice")
    with pytest.raises(HTTPException):
        env_client.doc_from_path(
            "./tests/data/expense_receipts/receipt.jpg",
        ).parse("financial_doc")
    with pytest.raises(HTTPException):
        env_client.doc_from_path("./tests/data/passport/passport.jpeg").parse(
            "passport"
        )
    with pytest.raises(HTTPException):
        env_client.doc_from_path("./tests/data/passport/passport.jpeg").parse("dummy")


def test_duplicate_configs(dummy_client):
    client = dummy_client.config_custom_doc(
        document_type="receipt",
        singular_name="dummy",
        plural_name="dummies",
        account_name="dummy",
    )
    assert isinstance(client, Client)
    with pytest.raises(RuntimeError):
        client.doc_from_path("./tests/data/expense_receipts/receipt.jpg").parse(
            "receipt"
        )


def test_parse_path_with_wrong_filetype(dummy_client):
    with pytest.raises(AssertionError):
        dummy_client.doc_from_path("./tests/data/expense_receipts/receipt.jpga").parse(
            "receipt"
        )
    with pytest.raises(AssertionError):
        dummy_client.doc_from_path("./tests/data/expense_receipts/receipt.jpga").parse(
            "invoice"
        )
    with pytest.raises(AssertionError):
        dummy_client.doc_from_path(
            "./tests/data/expense_receipts/receipt.jpga",
        ).parse("financial_doc")
    with pytest.raises(AssertionError):
        dummy_client.doc_from_path("./tests/data/expense_receipts/receipt.jpga").parse(
            "passport"
        )


def test_parse_path_with_wrong_token(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.doc_from_path("./tests/data/expense_receipts/receipt.jpg").parse(
            "receipt"
        )
    with pytest.raises(HTTPException):
        dummy_client.doc_from_path("./tests/data/expense_receipts/receipt.jpg").parse(
            "invoice"
        )
    with pytest.raises(HTTPException):
        dummy_client.doc_from_path(
            "./tests/data/expense_receipts/receipt.jpg",
        ).parse("financial_doc")
    with pytest.raises(HTTPException):
        dummy_client.doc_from_path("./tests/data/invoices/invoice.pdf").parse(
            "financial_doc"
        )
    with pytest.raises(HTTPException):
        dummy_client.doc_from_path("./tests/data/expense_receipts/receipt.jpg").parse(
            "passport"
        )


def test_response_load_failure():
    with pytest.raises(Exception):
        DocumentResponse.load("notAFile")


def test_request_with_filepath(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.doc_from_path("./tests/data/expense_receipts/receipt.jpg").parse(
            "receipt"
        )


def test_request_without_raise_on_error(dummy_client_no_raise):
    result = dummy_client_no_raise.doc_from_path(
        "./tests/data/expense_receipts/receipt.jpg"
    ).parse("receipt")
    assert result.receipt is None
    assert len(result.receipts) == 0


def test_request_without_raise_on_error_include_words(dummy_client_no_raise):
    result = dummy_client_no_raise.doc_from_path(
        "./tests/data/expense_receipts/receipt.jpg"
    ).parse("receipt", include_words=True)
    assert result.receipt is None
    assert len(result.receipts) == 0


def test_request_with_wrong_type(dummy_client):
    with pytest.raises(TypeError):
        dummy_client.doc_from_path(open("./tests/data/test.txt"))
    with pytest.raises(AttributeError):
        dummy_client.doc_from_file("./tests/data/test.txt")
    with pytest.raises(TypeError):
        dummy_client.doc_from_b64string(open("./tests/data/test.txt"), "test.jpg")


def test_interface_version():
    fixed_client = Client().config_custom_doc(
        document_type="dummy",
        singular_name="dummy",
        plural_name="dummies",
        account_name="dummy",
        api_key="dummy",
        version="1.1",
    )
    with pytest.raises(HTTPException):
        fixed_client.doc_from_path("./tests/data/expense_receipts/receipt.jpg").parse(
            "dummy"
        )
