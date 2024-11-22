import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.resume.resume_v1 import ResumeV1
from mindee.product.resume.resume_v1_document import (
    ResumeV1Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "resume" / "response_v1"

ResumeV1DocumentType = Document[
    ResumeV1Document,
    Page[ResumeV1Document],
]


@pytest.fixture
def complete_doc() -> ResumeV1DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(ResumeV1, json_data["document"])


@pytest.fixture
def empty_doc() -> ResumeV1DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(ResumeV1, json_data["document"])


def test_complete_doc(complete_doc: ResumeV1DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: ResumeV1DocumentType):
    prediction = empty_doc.inference.prediction
    assert prediction.document_language.value is None
    assert len(prediction.given_names) == 0
    assert len(prediction.surnames) == 0
    assert prediction.nationality.value is None
    assert prediction.email_address.value is None
    assert prediction.phone_number.value is None
    assert prediction.address.value is None
    assert len(prediction.social_networks_urls) == 0
    assert prediction.profession.value is None
    assert prediction.job_applied.value is None
    assert len(prediction.languages) == 0
    assert len(prediction.hard_skills) == 0
    assert len(prediction.soft_skills) == 0
    assert len(prediction.education) == 0
    assert len(prediction.professional_experiences) == 0
    assert len(prediction.certificates) == 0
