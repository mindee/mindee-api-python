import os

import pytest

from mindee import PathInput
from mindee.v2 import Client
from mindee.v2.error import MindeeHTTPErrorV2
from mindee.v2.product.extraction.rag_documents import (
    ExtractionRagAnnotationResponse,
    RagDocumentAnnotationParameters,
    RagDocumentUploadParameters,
)
from tests.utils import V2_PRODUCT_PATH


@pytest.mark.integration
@pytest.mark.v2
def test_rag_document_lifecycle_must_succeed():
    """Should perform the entire lifecycle of a RAG document."""
    extraction_model_id = os.getenv("MINDEE_V2_SE_TESTS_FINDOC_MODEL_ID")
    if extraction_model_id is None:
        raise RuntimeError(
            "MINDEE_V2_SE_TESTS_FINDOC_MODEL_ID environment variable is not set"
        )

    client = Client()

    input_source = PathInput(
        V2_PRODUCT_PATH / "extraction" / "financial_document" / "default_sample.jpg"
    )
    post_parameters = RagDocumentUploadParameters(model_id=extraction_model_id)
    post_response = client.upload_and_get_rag_document(input_source, post_parameters)
    assert post_response is not None

    post_annotation = post_response.annotation
    assert post_annotation is not None

    document_id = post_response.id
    assert document_id is not None

    assert post_response.status == "Draft"

    post_annotation.fields["supplier_name"].selected = True
    post_annotation.fields["supplier_name"].guidelines = "I am the walrus!"
    post_annotation.fields.get_simple_field("invoice_number").selected = True
    post_annotation.fields.get_simple_field(
        "invoice_number"
    ).guidelines = "koo koo katchoo!"

    patch_annotation_response = client.update_rag_annotations(
        RagDocumentAnnotationParameters(
            document_id=document_id,
            annotation=post_annotation,
        )
    )
    assert patch_annotation_response is not None
    patch_annotation = patch_annotation_response.annotation
    assert patch_annotation is not None

    assert (
        patch_annotation.fields.get_simple_field("supplier_name").guidelines
        == "I am the walrus!"
    )
    assert patch_annotation.fields.get_simple_field("supplier_name").selected is True
    assert (
        patch_annotation.fields.get_simple_field("invoice_number").guidelines
        == "koo koo katchoo!"
    )
    assert patch_annotation.fields.get_simple_field("invoice_number").selected is True

    get_response = client.get_ready_rag_document(
        ExtractionRagAnnotationResponse, document_id
    )
    assert get_response is not None
    get_annotation = get_response.annotation
    assert get_annotation is not None

    assert get_response.status == "Draft"

    assert (
        get_annotation.fields.get_simple_field("supplier_name").guidelines
        == "I am the walrus!"
    )
    assert get_annotation.fields.get_simple_field("supplier_name").selected is True
    assert (
        get_annotation.fields.get_simple_field("invoice_number").guidelines
        == "koo koo katchoo!"
    )
    assert get_annotation.fields.get_simple_field("invoice_number").selected is True

    patch_status_response = client.update_and_get_rag_annotations(
        RagDocumentAnnotationParameters(
            document_id=document_id,
            status="Active",
        )
    )
    assert patch_status_response is not None
    assert patch_status_response.status == "Active"

    delete_response = client.delete_extraction_rag_document(document_id)
    assert delete_response is True

    with pytest.raises(MindeeHTTPErrorV2):
        client.get_rag_document(ExtractionRagAnnotationResponse, document_id)
