from datetime import datetime, timezone

import pytest

from mindee.input import LocalResponse
from mindee.v2.search.rag_documents.rag_document_search_response import (
    RagDocumentSearchResponse,
)
from tests.utils import V2_DATA_DIR


@pytest.mark.v2
def test_should_load_search_rag_documents_locally():
    file_path = V2_DATA_DIR / "search" / "rag_documents.json"
    local_response = LocalResponse(file_path)
    response = local_response.deserialize_response(RagDocumentSearchResponse)

    assert isinstance(response, RagDocumentSearchResponse)

    assert len(response.rag_documents) == 3
    assert response.pagination.total_items == 3
    assert response.pagination.page == 1
    assert response.pagination.per_page == 50
    assert response.pagination.total_pages == 1

    first_item = response.rag_documents[0]
    assert first_item.id == "cc831599-c545-48b7-aa27-6d7ccd5b8d32"
    assert first_item.model_id == "12345678-1234-1234-1234-123456789abc"
    assert first_item.filename == "invoice_01.pdf"
    assert first_item.created_at == datetime(
        2026, 6, 30, 13, 13, 46, 168586, tzinfo=timezone.utc
    )
    assert first_item.total_matches == 0
    assert first_item.last_match_at is None
    assert first_item.status == "Processing"

    second_item = response.rag_documents[1]
    assert second_item.id == "27467e4c-5602-4315-90d9-3d2da69b05ab"
    assert second_item.model_id == "12345678-1234-1234-1234-123456789abc"
    assert second_item.filename == "invoice_02.pdf"
    assert second_item.created_at == datetime(
        2026, 6, 30, 13, 13, 46, 168586, tzinfo=timezone.utc
    )
    assert second_item.total_matches == 0
    assert second_item.last_match_at is None
    assert second_item.status == "Draft"

    third_item = response.rag_documents[2]
    assert third_item.id == "a6bcae7d-0439-476b-8a63-5a39ec05dc21"
    assert third_item.model_id == "12345678-1234-1234-1234-jobid1234567"
    assert third_item.filename == "invoice_03.pdf"
    assert third_item.created_at == datetime(
        2026, 6, 17, 14, 35, 46, 228006, tzinfo=timezone.utc
    )
    assert third_item.total_matches == 5
    assert third_item.last_match_at == datetime(
        2026, 6, 18, 14, 35, 46, 248006, tzinfo=timezone.utc
    )
    assert third_item.status == "Active"
