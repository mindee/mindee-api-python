from __future__ import annotations

import io
import logging
from typing import Any, BinaryIO

from mindee.dependencies.checkers import BERNARD_LEDIT_AVAILABLE, PILLOW_AVAILABLE
from mindee.dependencies.decorators import requires_bernard_ledit, requires_pillow
from mindee.image.image_compressor import compress_image
from mindee.pdf.pdf_utils import (
    lerp,
    pdf_has_source_text,
)

if BERNARD_LEDIT_AVAILABLE:
    # pylint: disable=import-error
    import bernard_ledit.pdf as bernard_pdf  # type: ignore[import-not-found]
else:
    bernard_pdf: Any = None  # type: ignore[no-redef] # pylint: disable=invalid-name

if PILLOW_AVAILABLE:
    # pylint: disable=import-error
    from PIL import Image
else:
    Image: Any = None  # type: ignore[no-redef] # pylint: disable=invalid-name

logger = logging.getLogger(__name__)
MIN_QUALITY = 1


@requires_bernard_ledit
def compress_pdf(
    pdf_data: BinaryIO | bytes,
    image_quality: int = 85,
    force_source_text_compression: bool = False,
    disable_source_text: bool = True,
) -> bytes:
    """
    Compresses each page of a provided PDF buffer.

    :param pdf_data: The input PDF as bytes.
    :param image_quality: Compression quality (70-100 for most JPG images).
    :param force_source_text_compression: If true, attempts to re-write detected text.
    :param disable_source_text: If true, doesn't re-apply source text to the output PDF.
    :return: Compressed PDF as bytes.
    """
    if not isinstance(pdf_data, bytes):
        pdf_bytes = pdf_data.read()
        pdf_data.seek(0)
    else:
        pdf_bytes = pdf_data

    if pdf_has_source_text(pdf_bytes):
        if force_source_text_compression:
            if not disable_source_text:
                logger.warning("Re-writing PDF source-text is an EXPERIMENTAL feature.")
            else:
                logger.warning(
                    "Source file contains text, but disable_source_text flag "
                    "is set to false. Resulting file will not contain any embedded text."
                )
        else:
            logger.warning(
                "Found text inside of the provided PDF file. Compression operation aborted since disableSourceText "
                "is set to 'true'."
            )
            return pdf_bytes

    if not disable_source_text:
        doc = bernard_pdf.PdfDocument(pdf_bytes)
        extracted_text = [page.chars() for page in doc]
    else:
        extracted_text = None

    compressed_pages = _compress_pdf_pages(pdf_bytes, image_quality)

    if not compressed_pages:
        logger.warning(
            "Could not compress PDF to a smaller size. Returning original PDF."
        )
        return pdf_bytes

    out_pdf = bernard_pdf.PdfDocument.new()
    out_pdf.append_multiple_jpeg_pages(
        [compressed_page_image[0] for compressed_page_image in compressed_pages]
    )

    if extracted_text:
        for i in range(len(out_pdf)):
            out_pdf.add_text(i, extracted_text[i])

    out_buffer = io.BytesIO()
    out_pdf.save(out_buffer)
    out_buffer.seek(0)
    return out_buffer.read()


def _compress_pdf_pages(
    pdf_data: bytes,
    image_quality: int,
) -> list[tuple[bytes, int, int]] | None:
    """
    Compresses PDF pages and returns an array of compressed page buffers.

    :param pdf_data: The input PDF as bytes.
    :param image_quality: Initial compression quality.
    :return: List of compressed page buffers, or None if compression fails.
    """
    original_size = len(pdf_data)
    image_quality_loop = image_quality

    while image_quality_loop >= MIN_QUALITY:
        compressed_pages = _compress_pages_with_quality(pdf_data, image_quality_loop)
        total_compressed_size = sum(len(page) for page in compressed_pages)

        if _is_compression_successful(
            total_compressed_size, original_size, image_quality
        ):
            return compressed_pages

        image_quality_loop -= round(lerp(1, 10, image_quality_loop / 100))

    return None


@requires_bernard_ledit
@requires_pillow
def _compress_pages_with_quality(
    pdf_data: bytes,
    image_quality: int,
) -> list[tuple[bytes, int, int]]:
    """
    Compresses pages with a specific quality.

    :param pdf_data: The input PDF as bytes.
    :param image_quality: Compression quality.
    :return: List of compressed page buffers.
    """
    pdf_document = bernard_pdf.PdfDocument(pdf_data)
    compressed_pages = []
    for index in range(len(pdf_document)):
        rasterized_page = pdf_document.rasterize_page(index, image_quality)
        compressed_image = compress_image(rasterized_page, image_quality)
        image = Image.open(io.BytesIO(compressed_image))
        compressed_pages.append((compressed_image, image.size[0], image.size[1]))

    return compressed_pages


def _is_compression_successful(
    total_compressed_size: int, original_size: int, image_quality: int
) -> bool:
    """
    Checks if the compression was successful based on the compressed size and original size.

    :param total_compressed_size: Total size of compressed pages.
    :param original_size: Original PDF size.
    :param image_quality: Compression quality.
    :return: True if compression was successful, false otherwise.
    """
    overhead = lerp(0.54, 0.18, image_quality / 100)
    return total_compressed_size + total_compressed_size * overhead < original_size
