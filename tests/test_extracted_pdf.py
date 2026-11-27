import io
from types import SimpleNamespace

import pytest

import mindee.pdf.extracted_pdf as extracted_pdf_module
from mindee.pdf.extracted_pdf import ExtractedPDF


@pytest.mark.parametrize(
    ("filename", "expected_filename", "extension"),
    [
        ("document.jpg", "document.jpg.pdf", ".jpg"),
        ("document.pdf", "document.pdf", ".pdf"),
        ("document", "document.pdf", ""),
    ],
)
def test_write_to_file_normalizes_pdf_extension(
    monkeypatch, tmp_path, filename: str, expected_filename: str, extension: str
):
    seen_extensions = []

    def format_from_extension(value: str) -> str:
        seen_extensions.append(value)
        return "PDF" if value.lower() == ".pdf" else "JPEG"

    monkeypatch.setattr(
        extracted_pdf_module,
        "bernard_common",
        SimpleNamespace(format_from_extension=format_from_extension),
    )
    extracted_pdf = ExtractedPDF(io.BytesIO(b"%PDF-content"), filename, [0])

    extracted_pdf.write_to_file(tmp_path)

    assert (tmp_path / expected_filename).read_bytes() == b"%PDF-content"
    assert seen_extensions == [extension]
