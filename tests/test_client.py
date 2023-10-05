import binascii
import pytest

from mindee import Client, PageOptions, product
from mindee.http.error import HTTPException
from mindee.input.sources import LocalInputSource
from mindee.parsing.common.predict_response import PredictResponse
from mindee.product.receipt.receipt_v4 import ReceiptV4
from tests import INVOICE_DATA_DIR
from tests.test_inputs import FILE_TYPES_DIR, PDF_DATA_DIR
from tests.utils import clear_envvars, dummy_envvars


@pytest.fixture
def empty_client(monkeypatch) -> Client:
    clear_envvars(monkeypatch)
    return Client()


@pytest.fixture
def env_client(monkeypatch) -> Client:
    dummy_envvars(monkeypatch)
    return Client("dummy")


@pytest.fixture
def dummy_client() -> Client:
    return Client("dummy")


def test_parse_path_without_token(empty_client: Client):
    with pytest.raises(RuntimeError):
        input_doc = empty_client.source_from_path(f"{PDF_DATA_DIR}/blank.pdf")
        empty_client.parse(product.ReceiptV4, input_doc)


def test_parse_path_with_env_token(env_client: Client):
    with pytest.raises(HTTPException):
        input_doc = env_client.source_from_path(f"{PDF_DATA_DIR}/blank.pdf")
        env_client.parse(product.ReceiptV4, input_doc)


def test_parse_path_with_wrong_filetype(dummy_client: Client):
    with pytest.raises(AssertionError):
        dummy_client.source_from_path(f"{FILE_TYPES_DIR}/receipt.jpga")


def test_parse_path_with_wrong_token(dummy_client: Client):
    with pytest.raises(HTTPException):
        input_doc = dummy_client.source_from_path(f"{PDF_DATA_DIR}/blank.pdf")
        dummy_client.parse(product.ReceiptV4, input_doc)


def test_request_with_wrong_type(dummy_client: Client):
    with pytest.raises(FileNotFoundError):
        dummy_client.source_from_path(open("./tests/data/test.txt").read())
    with pytest.raises(binascii.Error):
        dummy_client.source_from_b64string("./tests/data/test.txt", "test.jpg")


def test_interface_version(dummy_client: Client):
    dummy_endpoint = dummy_client.create_endpoint(
        endpoint_name="dummy",
        account_name="dummy",
        version="1.1",
    )
    with pytest.raises(HTTPException):
        input_doc = dummy_client.source_from_path(f"{FILE_TYPES_DIR}/receipt.jpg")
        dummy_client.parse(product.TypeCustomV1, input_doc, endpoint=dummy_endpoint)


def test_keep_file_open(dummy_client: Client):
    input_doc: LocalInputSource = dummy_client.source_from_path(
        f"{FILE_TYPES_DIR}/receipt.jpg"
    )
    try:
        dummy_client.parse(product.ReceiptV4, input_doc, close_file=False)
    except HTTPException:
        pass
    assert not input_doc.file_object.closed
    input_doc.close()
    assert input_doc.file_object.closed


def test_cut_options(dummy_client: Client):
    input_doc: LocalInputSource = dummy_client.source_from_path(
        f"{INVOICE_DATA_DIR}/invoice_10p.pdf"
    )
    try:
        # need to keep file open to count the pages after parsing
        dummy_client.parse(
            ReceiptV4,
            input_doc,
            close_file=False,
            page_options=PageOptions(page_indexes=range(5)),
        )
    except HTTPException:
        pass
    assert input_doc.count_doc_pages() == 5
    input_doc.close()
