import io
import logging
from ctypes import c_char_p, c_ushort
from threading import RLock
from typing import BinaryIO, List, Optional, Union

import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
from _ctypes import POINTER

from mindee.image_operations.image_compressor import compress_image
from mindee.pdf.pdf_char_data import PDFCharData
from mindee.pdf.pdf_utils import (
    attach_images_as_new_file,
    extract_text_from_pdf,
    has_source_text,
)

logger = logging.getLogger(__name__)
MIN_QUALITY = 1


def compress_pdf(
    pdf_data: Union[BinaryIO, bytes],
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

    if has_source_text(pdf_bytes):
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

    extracted_text = (
        extract_text_from_pdf(pdf_bytes) if not disable_source_text else None
    )

    compressed_pages = compress_pdf_pages(
        pdf_bytes, extracted_text, image_quality, disable_source_text
    )

    if not compressed_pages:
        logger.warning(
            "Could not compress PDF to a smaller size. Returning original PDF."
        )
        return pdf_bytes

    out_pdf = attach_images_as_new_file(
        [io.BytesIO(compressed_page) for compressed_page in compressed_pages]
    )
    out_buffer = io.BytesIO()
    out_pdf.save(out_buffer)
    out_buffer.seek(0)
    return out_buffer.read()


def compress_pdf_pages(
    pdf_data: bytes,
    extracted_text: Optional[List[PDFCharData]],
    image_quality: int,
    disable_source_text: bool,
) -> Optional[List[bytes]]:
    """
    Compresses PDF pages and returns an array of compressed page buffers.

    :param pdf_data: The input PDF as bytes.
    :param extracted_text: Extracted text from the PDF.
    :param image_quality: Initial compression quality.
    :param disable_source_text: If true, doesn't re-apply source text to the output PDF.
    :return: List of compressed page buffers, or None if compression fails.
    """
    original_size = len(pdf_data)
    image_quality_loop = image_quality

    while image_quality_loop >= MIN_QUALITY:
        compressed_pages = compress_pages_with_quality(
            pdf_data, extracted_text, image_quality_loop, disable_source_text
        )
        total_compressed_size = sum(len(page) for page in compressed_pages)

        if is_compression_successful(
            total_compressed_size, original_size, image_quality
        ):
            return compressed_pages

        image_quality_loop -= round(lerp(1, 10, image_quality_loop / 100))

    return None


def add_text_to_pdf_page(  # type: ignore
    document: pdfium.PdfDocument,
    page_id: int,
    extracted_text: Optional[List[PDFCharData]],
) -> None:
    """
    Adds text to a PDF page based on the extracted text data.

    :param document: The PDFDocument object.
    :param page_id: ID of the current page.
    :param extracted_text: List of PDFCharData objects containing text and positioning information.
    """
    if not extracted_text:
        return

    height = document[page_id].get_height()
    pdfium_lock = RLock()

    with pdfium_lock:
        for char_data in extracted_text:
            font_name = c_char_p(char_data.font_name.encode("utf-8"))
            text_handler = pdfium_c.FPDFPageObj_NewTextObj(
                document.raw, font_name, char_data.font_size
            )
            char_code = ord(char_data.char)
            char_code_c_char = c_ushort(char_code)
            char_ptr = POINTER(c_ushort)(char_code_c_char)
            pdfium_c.FPDFText_SetText(text_handler, char_ptr)
            pdfium_c.FPDFPageObj_Transform(
                text_handler, 1, 0, 0, 1, char_data.left, height - char_data.top
            )
            pdfium_c.FPDFPage_InsertObject(document[page_id].raw, text_handler)
            pdfium_c.FPDFPageObj_Destroy(text_handler)
        pdfium_c.FPDFPage_GenerateContent(document[page_id].raw)
        pdfium_c.FPDF_ClosePage(document[page_id].raw)


def compress_pages_with_quality(
    pdf_data: bytes,
    extracted_text: Optional[list[PDFCharData]],
    image_quality: int,
    disable_source_text: bool,
) -> List[bytes]:
    """
    Compresses pages with a specific quality.

    :param pdf_data: The input PDF as bytes.
    :param extracted_text: Extracted text from the PDF.
    :param image_quality: Compression quality.
    :param disable_source_text: If true, doesn't re-apply source text to the output PDF.
    :return: List of compressed page buffers.
    """
    pdf_document = pdfium.PdfDocument(pdf_data)
    compressed_pages = []

    for [i, page] in enumerate(pdf_document):
        rasterized_page = rasterize_page(page, image_quality)
        compressed_image = compress_image(rasterized_page, image_quality)

        if not disable_source_text:
            add_text_to_pdf_page(pdf_document, i, extracted_text)

        compressed_pages.append(compressed_image)

    return compressed_pages


def is_compression_successful(
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


def rasterize_page(  # type: ignore
    page: pdfium.PdfPage,
    quality: int = 85,
) -> bytes:
    """
    Rasterizes a PDF page.

    :param page: PdfPage object to rasterize.
    :param quality: Quality to apply during rasterization.
    :return: Rasterized page as bytes.
    """
    image = page.render().to_pil()
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=quality)
    return buffer.getvalue()


def lerp(start: float, end: float, t: float) -> float:
    """
    Performs linear interpolation between two numbers.

    :param start: The starting value.
    :param end: The ending value.
    :param t: The interpolation factor (0 to 1).
    :return: The interpolated value.
    """
    return start * (1 - t) + end * t
