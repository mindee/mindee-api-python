import binascii

import pytest

from mindee import AsyncPredictResponse, Client, PageOptions, PredictResponse, product
from mindee.error.mindee_error import MindeeClientError, MindeeError
from mindee.error.mindee_http_error import MindeeHTTPError
from mindee.input.local_response import LocalResponse
from mindee.input.sources.local_input_source import LocalInputSource
from mindee.product import MultiReceiptsDetectorV1
from mindee.product.international_id.international_id_v2 import InternationalIdV2
from mindee.product.invoice.invoice_v4 import InvoiceV4
from mindee.product.invoice_splitter.invoice_splitter_v1 import InvoiceSplitterV1
from mindee.product.receipt.receipt_v5 import ReceiptV5
from tests.mindee_http.test_error import ERROR_DATA_DIR
from tests.test_inputs import FILE_TYPES_DIR, PRODUCT_DATA_DIR
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
        input_doc = empty_client.source_from_path(FILE_TYPES_DIR / "pdf" / "blank.pdf")
        empty_client.parse(product.ReceiptV5, input_doc)


def test_parse_path_with_env_token(env_client: Client):
    with pytest.raises(MindeeHTTPError):
        input_doc = env_client.source_from_path(FILE_TYPES_DIR / "pdf" / "blank.pdf")
        env_client.parse(product.ReceiptV5, input_doc)


def test_parse_path_with_wrong_filetype(dummy_client: Client):
    with pytest.raises(AssertionError):
        dummy_client.source_from_path(FILE_TYPES_DIR / "receipt.jpga")


def test_parse_path_with_wrong_token(dummy_client: Client):
    with pytest.raises(MindeeHTTPError):
        input_doc = dummy_client.source_from_path(FILE_TYPES_DIR / "pdf" / "blank.pdf")
        dummy_client.parse(product.ReceiptV5, input_doc)


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
    with pytest.raises(MindeeHTTPError):
        input_doc = dummy_client.source_from_path(FILE_TYPES_DIR / "receipt.jpg")
        dummy_client.parse(product.CustomV1, input_doc, endpoint=dummy_endpoint)


def test_keep_file_open(dummy_client: Client):
    input_doc: LocalInputSource = dummy_client.source_from_path(
        f"{FILE_TYPES_DIR}/receipt.jpg"
    )
    try:
        dummy_client.parse(product.ReceiptV5, input_doc, close_file=False)
    except MindeeHTTPError:
        pass
    assert not input_doc.file_object.closed
    input_doc.close()
    assert input_doc.file_object.closed


def test_cut_options(dummy_client: Client):
    input_doc: LocalInputSource = dummy_client.source_from_path(
        f"{FILE_TYPES_DIR}/pdf/multipage.pdf"
    )
    try:
        # need to keep file open to count the pages after parsing
        dummy_client.parse(
            ReceiptV5,
            input_doc,
            close_file=False,
            page_options=PageOptions(page_indexes=range(5)),
        )
    except MindeeHTTPError:
        pass
    assert input_doc.count_doc_pages() == 5
    input_doc.close()


def test_async_wrong_initial_delay(dummy_client: Client):
    input_doc = dummy_client.source_from_path(FILE_TYPES_DIR / "pdf" / "blank.pdf")
    with pytest.raises(MindeeClientError):
        dummy_client.enqueue_and_parse(
            InvoiceSplitterV1, input_doc, initial_delay_sec=0
        )


def test_async_wrong_polling_delay(dummy_client: Client):
    input_doc = dummy_client.source_from_path(FILE_TYPES_DIR / "pdf" / "blank.pdf")
    with pytest.raises(MindeeClientError):
        dummy_client.enqueue_and_parse(InvoiceSplitterV1, input_doc, delay_sec=0)


def test_local_response_from_sync_json(dummy_client: Client):
    input_file = LocalResponse(
        PRODUCT_DATA_DIR / "multi_receipts_detector" / "response_v1" / "complete.json"
    )
    with open(
        PRODUCT_DATA_DIR
        / "multi_receipts_detector"
        / "response_v1"
        / "summary_full.rst"
    ) as f:
        reference_doc = f.read()
    result = dummy_client.load_prediction(MultiReceiptsDetectorV1, input_file)
    assert isinstance(result, PredictResponse)
    assert str(result.document) == reference_doc


def test_local_response_from_async_json(dummy_client: Client):
    input_file = LocalResponse(
        PRODUCT_DATA_DIR / "international_id" / "response_v2" / "complete.json"
    )
    with open(
        PRODUCT_DATA_DIR / "international_id" / "response_v2" / "summary_full.rst"
    ) as f:
        reference_doc = f.read()
    result = dummy_client.load_prediction(InternationalIdV2, input_file)
    assert isinstance(result, AsyncPredictResponse)
    assert str(result.document) == reference_doc


def test_local_response_from_invalid_file(dummy_client: Client):
    local_response = LocalResponse(
        PRODUCT_DATA_DIR / "invoices" / "response_v4" / "summary_full.rst"
    )
    with pytest.raises(MindeeError):
        print(local_response.as_dict)


def test_local_response_from_invalid_dict(dummy_client: Client):
    input_file = LocalResponse(ERROR_DATA_DIR / "error_400_no_details.json")
    with pytest.raises(MindeeError):
        dummy_client.load_prediction(InvoiceV4, input_file)
