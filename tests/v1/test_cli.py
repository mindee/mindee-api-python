import json
from argparse import Namespace

import pytest

from mindee.commands.cli_parser import MindeeParser
from mindee.error.mindee_http_error import MindeeHTTPClientError, MindeeHTTPError
from tests.utils import clear_envvars


@pytest.fixture
def custom_doc(monkeypatch):
    clear_envvars(monkeypatch)
    return Namespace(
        product_name="custom",
        endpoint_name="license_plate",
        account_name="mindee",
        api_key="dummy",
        api_version="1",
        cut_doc=False,
        doc_pages=3,
        input_type="path",
        output_type="summary",
        include_words=False,
        path="./tests/data/file_types/pdf/blank.pdf",
        parse_type="parse",
        async_parse=False,
    )


@pytest.fixture
def generated_doc_sync(monkeypatch):
    clear_envvars(monkeypatch)
    return Namespace(
        product_name="generated",
        endpoint_name="license_plate",
        account_name="mindee",
        api_key="dummy",
        api_version="1",
        cut_doc=False,
        doc_pages=3,
        input_type="path",
        output_type="summary",
        include_words=False,
        path="./tests/data/file_types/pdf/blank.pdf",
        parse_type="parse",
        async_parse=False,
    )


@pytest.fixture
def generated_doc_async(monkeypatch):
    clear_envvars(monkeypatch)
    return Namespace(
        product_name="generated",
        endpoint_name="invoice_splitter",
        account_name="mindee",
        api_key="dummy",
        api_version="1",
        cut_doc=False,
        doc_pages=3,
        input_type="path",
        output_type="summary",
        include_words=False,
        path="./tests/data/file_types/pdf/blank.pdf",
        parse_type="parse",
        async_parse=True,
    )


@pytest.fixture
def ots_doc(monkeypatch):
    clear_envvars(monkeypatch)
    return Namespace(
        api_key="dummy",
        product_name="invoice",
        cut_doc=False,
        doc_pages=3,
        input_type="path",
        output_type="summary",
        include_words=False,
        path="./tests/data/products/invoices/invoice.pdf",
        parse_type="parse",
        async_parse=False,
    )


@pytest.fixture
def ots_doc_enqueue_and_parse(monkeypatch):
    clear_envvars(monkeypatch)
    return Namespace(
        api_key="dummy",
        product_name="invoice-splitter",
        cut_doc=False,
        doc_pages=3,
        input_type="path",
        include_words=False,
        path="./tests/data/products/invoice_splitter/default_sample.pdf",
        parse_type="parse",
        async_parse=True,
    )


@pytest.fixture
def ots_doc_feedback(monkeypatch):
    clear_envvars(monkeypatch)
    dummy_feedback = '{"feedback": {"dummy_field": {"value": "dummy"}}}'
    return Namespace(
        api_key="dummy",
        output_type="summary",
        product_name="custom",
        endpoint_name="dummy-endpoint",
        account_name="dummy",
        api_version="dummy",
        queue_id="dummy-queue-id",
        call_method="parse-queued",
        input_type="path",
        path="./tests/data/file_types/pdf/blank.pdf",
        parse_type="feedback",
        feedback=json.loads(dummy_feedback),
    )


def test_cli_custom_doc(custom_doc):
    with pytest.raises(MindeeHTTPError):
        parser = MindeeParser(parsed_args=custom_doc)
        parser.call_endpoint()


def test_cli_generated_doc_sync(generated_doc_sync):
    with pytest.raises(MindeeHTTPError):
        parser = MindeeParser(parsed_args=generated_doc_sync)
        parser.call_endpoint()


def test_cli_generated_doc_async(generated_doc_async):
    with pytest.raises(MindeeHTTPError):
        parser = MindeeParser(parsed_args=generated_doc_async)
        parser.call_endpoint()


def test_cli_invoice(ots_doc):
    ots_doc.product_name = "invoice"
    ots_doc.api_key = ""
    with pytest.raises(RuntimeError):
        parser = MindeeParser(parsed_args=ots_doc)
        parser.call_endpoint()
    ots_doc.api_key = "dummy"
    with pytest.raises(MindeeHTTPError):
        parser = MindeeParser(parsed_args=ots_doc)
        parser.call_endpoint()


def test_cli_receipt(ots_doc):
    ots_doc.product_name = "receipt"
    ots_doc.api_key = ""
    with pytest.raises(RuntimeError):
        parser = MindeeParser(parsed_args=ots_doc)
        parser.call_endpoint()
    ots_doc.api_key = "dummy"
    with pytest.raises(MindeeHTTPError):
        parser = MindeeParser(parsed_args=ots_doc)
        parser.call_endpoint()


def test_cli_financial_doc(ots_doc):
    ots_doc.product_name = "financial-document"
    ots_doc.api_key = ""
    with pytest.raises(RuntimeError):
        parser = MindeeParser(parsed_args=ots_doc)
        parser.call_endpoint()
    ots_doc.api_key = "dummy"
    with pytest.raises(MindeeHTTPError):
        parser = MindeeParser(parsed_args=ots_doc)
        parser.call_endpoint()


def test_cli_passport(ots_doc):
    ots_doc.product_name = "passport"
    ots_doc.api_key = ""
    with pytest.raises(RuntimeError):
        parser = MindeeParser(parsed_args=ots_doc)
        parser.call_endpoint()
    ots_doc.api_key = "dummy"
    with pytest.raises(MindeeHTTPError):
        parser = MindeeParser(parsed_args=ots_doc)
        parser.call_endpoint()


def test_cli_us_bank_check(ots_doc):
    ots_doc.product_name = "us-bank-check"
    ots_doc.api_key = ""
    with pytest.raises(RuntimeError):
        parser = MindeeParser(parsed_args=ots_doc)
        parser.call_endpoint()
    ots_doc.api_key = "dummy"
    with pytest.raises(MindeeHTTPError):
        parser = MindeeParser(parsed_args=ots_doc)
        parser.call_endpoint()


def test_cli_invoice_splitter_enqueue(ots_doc_enqueue_and_parse):
    ots_doc_enqueue_and_parse.product_name = "invoice-splitter"
    ots_doc_enqueue_and_parse.api_key = ""
    with pytest.raises(RuntimeError):
        parser = MindeeParser(parsed_args=ots_doc_enqueue_and_parse)
        parser.call_endpoint()
    ots_doc_enqueue_and_parse.api_key = "dummy"
    with pytest.raises(MindeeHTTPError):
        parser = MindeeParser(parsed_args=ots_doc_enqueue_and_parse)
        parser.call_endpoint()


def test_cli_feedback(ots_doc_feedback):
    ots_doc_feedback.document_id = "dummy-document-id"
    ots_doc_feedback.api_key = ""
    with pytest.raises(RuntimeError):
        parser = MindeeParser(parsed_args=ots_doc_feedback)
        parser.call_endpoint()
    ots_doc_feedback.api_key = "dummy"
    with pytest.raises(MindeeHTTPClientError):
        parser = MindeeParser(parsed_args=ots_doc_feedback)
        parser.call_endpoint()
