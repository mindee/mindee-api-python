import pytest

from mindee import Client, PageOptions, PredictResponse
from mindee.endpoints import HTTPException
from tests import INVOICE_DATA_DIR, PASSPORT_DATA_DIR, RECEIPT_DATA_DIR
from tests.utils import clear_envvars, dummy_envvars


@pytest.fixture
def empty_client(monkeypatch):
    clear_envvars(monkeypatch)
    return Client().add_endpoint(
        endpoint_name="dummy",
        account_name="dummy",
    )


@pytest.fixture
def env_client(monkeypatch):
    dummy_envvars(monkeypatch)
    return Client("dummy").add_endpoint(
        endpoint_name="dummy",
        account_name="dummy",
    )


@pytest.fixture
def dummy_client():
    return Client("dummy").add_endpoint(
        endpoint_name="dummy",
        account_name="dummy",
    )


@pytest.fixture
def dummy_client_no_raise():
    return Client(api_key="dummy", raise_on_error=False)


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
    client = dummy_client.add_endpoint(
        endpoint_name="receipt",
        account_name="dummy",
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
        PredictResponse.load("notAFile")


def test_request_with_filepath(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.doc_from_path(f"{RECEIPT_DATA_DIR}/receipt.jpg").parse("receipt")


def test_request_without_raise_on_error(dummy_client_no_raise):
    result = dummy_client_no_raise.doc_from_path(
        f"{RECEIPT_DATA_DIR}/receipt.jpg"
    ).parse("receipt")
    assert result.document is None
    assert len(result.pages) == 0


def test_request_without_raise_on_error_include_words(dummy_client_no_raise):
    result = dummy_client_no_raise.doc_from_path(
        f"{RECEIPT_DATA_DIR}/receipt.jpg"
    ).parse("receipt", include_words=True)
    assert result.document is None
    assert len(result.pages) == 0


def test_request_with_wrong_type(dummy_client):
    with pytest.raises(TypeError):
        dummy_client.doc_from_path(open("./tests/data/test.txt"))
    with pytest.raises(AttributeError):
        dummy_client.doc_from_file("./tests/data/test.txt")
    with pytest.raises(TypeError):
        dummy_client.doc_from_b64string(open("./tests/data/test.txt"), "test.jpg")


def test_interface_version():
    fixed_client = Client("dummy").add_endpoint(
        endpoint_name="dummy",
        account_name="dummy",
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


def test_cut_options(dummy_client):
    doc = dummy_client.doc_from_path(f"{INVOICE_DATA_DIR}/invoice_10p.pdf")
    try:
        # need to keep file open to count the pages after parsing
        doc.parse(
            "invoice", close_file=False, page_options=PageOptions(page_indexes=range(5))
        )
    except HTTPException:
        pass
    assert doc.input_doc.count_doc_pages() == 5
    doc.close()
