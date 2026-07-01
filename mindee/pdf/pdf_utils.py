from __future__ import annotations

from typing import Any

from mindee.dependencies.checkers import BERNARD_LEDIT_AVAILABLE
from mindee.dependencies.decorators import requires_bernard_ledit

if BERNARD_LEDIT_AVAILABLE:
    # pylint: disable=import-error
    import bernard_ledit.pdf as bernard_pdf  # type: ignore[import-not-found]
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


def _adjust_char_box(
    char_box: tuple[float, float, float, float],
    rotation: int,
    internal_height: float,
    internal_width: float,
) -> tuple[float, float, float, float]:
    """
    Adjusts the character bounding box based on page rotation.

    :param char_box: The original character bounding box.
    :param rotation: The page rotation in degrees.
    :param internal_height: The height of the page.
    :param internal_width: The width of the page.
    :return: The adjusted character bounding box.
    """
    left, right, bottom, top = char_box
    if rotation == 0:
        top, bottom = internal_height - top, internal_height - bottom
    elif rotation == 90:
        left, right, top, bottom = bottom, top, left, right
    elif rotation == 180:
        left, right = internal_width - right, internal_width - left
        top, bottom = bottom, top
    elif rotation == 270:
        left, right, top, bottom = (
            internal_width - top,
            internal_width - bottom,
            internal_height - right,
            internal_height - left,
        )
    return left, right, top, bottom


def lerp(start: float, end: float, t: float) -> float:
    """
    Performs linear interpolation between two numbers.

    :param start: The starting value.
    :param end: The ending value.
    :param t: The interpolation factor (0 to 1).
    :return: The interpolated value.
    """
    return start * (1 - t) + end * t
