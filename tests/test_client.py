import pytest
from mindee import Client, Response, Receipt, Passport
from mindee.http import HTTPException


@pytest.fixture
def empty_client():
    return Client()


@pytest.fixture
def dummy_client():
    return Client(
        expense_receipt_token="dummy",
        invoice_token="dummy",
        passport_token="dummy",
        license_plate_token="dummy",
    )


@pytest.fixture
def dummy_client_dont_raise():
    return Client(
        expense_receipt_token="dummy",
        invoice_token="dummy",
        passport_token="dummy",
        license_plate_token="dummy",
        raise_on_error=False,
    )


@pytest.fixture
def response():
    return Response.load("./tests/data/expense_receipts/v3/receipt.json")


def test_parse_receipt_without_token(empty_client):
    with pytest.raises(Exception):
        empty_client.parse_receipt("./tests/data/expense_receipts/receipt.jpg")


def test_parse_invoice_without_token(empty_client):
    with pytest.raises(Exception):
        empty_client.parse_invoice("./tests/data/expense_receipts/receipt.jpg")


def test_parse_financial_doc_without_token(empty_client):
    with pytest.raises(Exception):
        empty_client.parse_financial_document(
            "./tests/data/expense_receipts/receipt.jpg"
        )


def test_parse_passport_without_token(empty_client):
    with pytest.raises(Exception):
        empty_client.parse_passport("./tests/data/expense_receipts/receipt.jpg")


def test_parse_license_plate_without_token(empty_client):
    with pytest.raises(Exception):
        empty_client.parse_license_plate("./tests/data/license_plates/plate.png")


def test_parse_receipt_with_wrong_filetype(dummy_client):
    with pytest.raises(AssertionError):
        dummy_client.parse_receipt("./tests/data/expense_receipts/receipt.jpga")


def test_parse_invoice_with_wrong_filetype(dummy_client):
    with pytest.raises(AssertionError):
        dummy_client.parse_invoice("./tests/data/expense_receipts/receipt.jpga")


def test_parse_financial_doc_with_wrong_filetype(dummy_client):
    with pytest.raises(AssertionError):
        dummy_client.parse_financial_document(
            "./tests/data/expense_receipts/receipt.jpga"
        )


def test_parse_passport_with_wrong_filetype(dummy_client):
    with pytest.raises(AssertionError):
        dummy_client.parse_passport("./tests/data/expense_receipts/receipt.jpga")


def test_parse_plate_with_wrong_filetype(dummy_client):
    with pytest.raises(AssertionError):
        dummy_client.parse_license_plate("./tests/data/expense_receipts/receipt.jpga")


def test_parse_receipt_with_wrong_token(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.parse_receipt("./tests/data/expense_receipts/receipt.jpg")


def test_parse_receipt_with_wrong_version(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.parse_receipt(
            "./tests/data/expense_receipts/receipt.jpg", version="4000"
        )


def test_parse_invoice_with_wrong_token(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.parse_invoice("./tests/data/expense_receipts/receipt.jpg")


def test_parse_financial_doc_with_wrong_token_jpg(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.parse_financial_document(
            "./tests/data/expense_receipts/receipt.jpg"
        )


def test_parse_financial_doc_with_wrong_token_pdf(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.parse_financial_document("./tests/data/invoices/invoice.pdf")


def test_parse_passport_with_wrong_token(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.parse_passport("./tests/data/expense_receipts/receipt.jpg")


def test_parse_license_plate_with_wrong_token(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.parse_license_plate("./tests/data/license_plates/plate.png")


def test_response_dump(response):
    assert isinstance(response.receipt, Receipt)
    response.dump("./tests/data/response_dump.json")


def test_response_dump_failure(response):
    with pytest.raises(Exception):
        response.dump(open("./tests/pathDoesNotExist/aaa"))


def test_response_load_failure():
    with pytest.raises(Exception):
        Response.load("notAFile")


def test_response_with_passport_type():
    response = Response.load("./tests/data/passport/v1/passport.json")
    assert isinstance(response.passport, Passport)


def test_request_with_filepath(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.parse_receipt(
            "./tests/data/expense_receipts/receipt.jpg", input_type="path"
        )


def test_request_with_file(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.parse_receipt(
            open("./tests/data/expense_receipts/receipt.jpg", "rb"), input_type="stream"
        )


def test_request_with_base64_no_filename(dummy_client):
    with open("./tests/data/expense_receipts/receipt.txt", "r") as fh:
        b64 = fh.read()
    with pytest.raises(AssertionError):
        dummy_client.parse_receipt(b64, input_type="base64")


def test_request_with_base64(dummy_client):
    with open("./tests/data/expense_receipts/receipt.txt", "r") as fh:
        b64 = fh.read()
    with pytest.raises(HTTPException):
        dummy_client.parse_receipt(b64, input_type="base64", filename="receipt.txt")


def test_request_without_raise_on_error(dummy_client_dont_raise):
    result = dummy_client_dont_raise.parse_receipt(
        "./tests/data/expense_receipts/receipt.jpg", input_type="path"
    )
    assert result.receipt is None
    assert len(result.receipts) == 0


def test_request_without_raise_on_error_include_words(dummy_client_dont_raise):
    result = dummy_client_dont_raise.parse_receipt(
        "./tests/data/expense_receipts/receipt.jpg",
        input_type="path",
        include_words=True,
    )
    assert result.receipt is None
    assert len(result.receipts) == 0


def test_request_with_file_wrong_type(dummy_client):
    with pytest.raises(AssertionError):
        dummy_client.parse_receipt(open("./tests/data/test.txt"), input_type="file")

    with pytest.raises(AssertionError):
        dummy_client.parse_receipt("./tests/data/test.txt", input_type="path")


def test_pdf_reconstruct(dummy_client):
    with pytest.raises(HTTPException):
        dummy_client.parse_invoice("./tests/data/invoices/invoice_6p.pdf")
