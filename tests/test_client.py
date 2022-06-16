import pytest

from mindee import Client, DocumentResponse
from mindee.endpoints import HTTPException
from tests import INVOICE_DATA_DIR, PASSPORT_DATA_DIR, RECEIPT_DATA_DIR
from tests.utils import clear_envvars, dummy_envvars


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


def test_parse_path_without_token(empty_client):
    with pytest.raises(RuntimeError):
        empty_client.doc_from_path(f"{RECEIPT_DATA_DIR}/receipt.jpg").parse("receipt")
    with pytest.raises(RuntimeError):
        empty_client.doc_from_path(f"{INVOICE_DATA_DIR}/invoice.pdf").parse("invoice")
    with pytest.raises(RuntimeError):
        empty_client.doc_from_path(f"{RECEIPT_DATA_DIR}/receipt.jpg").parse(
            "financial_doc"
        )
    with pytest.raises(RuntimeError):
        empty_client.doc_from_path(f"{PASSPORT_DATA_DIR}/passport.jpeg").parse(
            "passport"
        )


def test_parse_path_with_env_token(env_client):
    with pytest.raises(HTTPException):
        env_client.doc_from_path(f"{RECEIPT_DATA_DIR}/receipt.jpg").parse("receipt")
    with pytest.raises(HTTPException):
        env_client.doc_from_path(f"{INVOICE_DATA_DIR}/invoice.pdf").parse("invoice")
    with pytest.raises(HTTPException):
        env_client.doc_from_path(
            f"{RECEIPT_DATA_DIR}/receipt.jpg",
        ).parse("financial_doc")
    with pytest.raises(HTTPException):
        env_client.doc_from_path(f"{PASSPORT_DATA_DIR}/passport.jpeg").parse("passport")
    with pytest.raises(HTTPException):
        env_client.doc_from_path(f"{PASSPORT_DATA_DIR}/passport.jpeg").parse("dummy")


def test_duplicate_configs(dummy_client):
    client = dummy_client.config_custom_doc(
        document_type="receipt",
        singular_name="dummy",
        plural_name="dummies",
        account_name="dummy",
        api_key="invalid",
    )
    assert isinstance(client, Client)
    with pytest.raises(RuntimeError):
        client.doc_from_path(f"{RECEIPT_DATA_DIR}/receipt.jpg").parse("receipt")
    with pytest.raises(HTTPException):
        client.doc_from_path(f"{RECEIPT_DATA_DIR}/receipt.jpg").parse(
            "receipt", "dummy"
        )


def test_parse_path_with_wrong_filetype(dummy_client):
    with pytest.raises(AssertionError):
        dummy_client.doc_from_path(f"{RECEIPT_DATA_DIR}/receipt.jpga").parse("receipt")
    with pytest.raises(AssertionError):
        dummy_client.doc_from_path(f"{RECEIPT_DATA_DIR}/receipt.jpga").parse("invoice")
    with pytest.raises(AssertionError):
        dummy_client.doc_from_path(
            f"{RECEIPT_DATA_DIR}/receipt.jpga",
        ).parse("financial_doc")
    with pytest.raises(AssertionError):
        dummy_client.doc_from_path(f"{RECEIPT_DATA_DIR}/receipt.jpga").parse("passport")


def test_parse_path_with_wrong_token(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.doc_from_path(f"{RECEIPT_DATA_DIR}/receipt.jpg").parse("receipt")
    with pytest.raises(HTTPException):
        dummy_client.doc_from_path(f"{RECEIPT_DATA_DIR}/receipt.jpg").parse("invoice")
    with pytest.raises(HTTPException):
        dummy_client.doc_from_path(
            f"{RECEIPT_DATA_DIR}/receipt.jpg",
        ).parse("financial_doc")
    with pytest.raises(HTTPException):
        dummy_client.doc_from_path(f"{INVOICE_DATA_DIR}/invoice.pdf").parse(
            "financial_doc"
        )
    with pytest.raises(HTTPException):
        dummy_client.doc_from_path(f"{RECEIPT_DATA_DIR}/receipt.jpg").parse("passport")


def test_response_load_failure():
    with pytest.raises(Exception):
        DocumentResponse.load("notAFile")


def test_request_with_filepath(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.doc_from_path(f"{RECEIPT_DATA_DIR}/receipt.jpg").parse("receipt")


def test_request_without_raise_on_error(dummy_client_no_raise):
    result = dummy_client_no_raise.doc_from_path(
        f"{RECEIPT_DATA_DIR}/receipt.jpg"
    ).parse("receipt")
    assert result.receipt is None
    assert len(result.receipts) == 0


def test_request_without_raise_on_error_include_words(dummy_client_no_raise):
    result = dummy_client_no_raise.doc_from_path(
        f"{RECEIPT_DATA_DIR}/receipt.jpg"
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
        fixed_client.doc_from_path(f"{RECEIPT_DATA_DIR}/receipt.jpg").parse("dummy")


def test_keep_file_open(dummy_client):
    doc = dummy_client.doc_from_path(f"{RECEIPT_DATA_DIR}/receipt.jpg")
    try:
        doc.parse("receipt", close_file=False)
    except HTTPException:
        pass
    assert not doc.input_doc.file_object.closed
    doc.close()
    assert doc.input_doc.file_object.closed
