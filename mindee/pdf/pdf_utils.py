from __future__ import annotations

from typing import Any

from mindee.dependencies.checkers import BERNARD_LEDIT_AVAILABLE
from mindee.dependencies.decorators import requires_bernard_ledit

if BERNARD_LEDIT_AVAILABLE:
    # pylint: disable=import-error
    import bernard_ledit.pdf as bernard_pdf
else:
    bernard_pdf: Any = None  # type: ignore[no-redef] # pylint: disable=invalid-name


@requires_bernard_ledit
def pdf_has_source_text(pdf_bytes: bytes) -> bool:
    """
    Checks if the provided PDF bytes contain source text.

    :param pdf_bytes: Raw bytes representation of a PDF file
    :return: True if source text is found, False otherwise.
    """
    pdf = bernard_pdf.PdfDocument(pdf_bytes)

    try:
        return pdf.has_text()
    finally:
        if hasattr(pdf, "close"):
            pdf.close()
