import io
import logging
from ctypes import c_char_p, c_ushort
from threading import RLock
from typing import BinaryIO, List, Optional, Tuple, Union

import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
from _ctypes import POINTER
from PIL import Image

from mindee.image_operations.image_compressor import compress_image
from mindee.pdf.pdf_char_data import PDFCharData
from mindee.pdf.pdf_utils import (
    extract_text_from_pdf,
    has_source_text,
    lerp,
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

    compressed_pages = _compress_pdf_pages(pdf_bytes, image_quality)

    if not compressed_pages:
        logger.warning(
            "Could not compress PDF to a smaller size. Returning original PDF."
        )
        return pdf_bytes

    out_pdf = _collect_images_as_pdf(
        [compressed_page_image[0] for compressed_page_image in compressed_pages]
    )

    if not disable_source_text:
        for i, page in enumerate(out_pdf):
            add_text_to_pdf_page(page, i, extracted_text)

    out_buffer = io.BytesIO()
    out_pdf.save(out_buffer)
    out_buffer.seek(0)
    return out_buffer.read()


def _compress_pdf_pages(
    pdf_data: bytes,
    image_quality: int,
) -> Optional[List[Tuple[bytes, int, int]]]:
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


def add_text_to_pdf_page(  # type: ignore
    page: pdfium.PdfPage,
    page_id: int,
    extracted_text: Optional[List[List[PDFCharData]]],
) -> None:
    """
    Adds text to a PDF page based on the extracted text data.

    :param page: The PDFDocument object.
    :param page_id: The ID of the page.
    :param extracted_text: List of PDFCharData objects containing text and positioning information.
    """
    if not extracted_text or not extracted_text[page_id]:
        return

    height = page.get_height()
    pdfium_lock = RLock()

    with pdfium_lock:
        for char_data in extracted_text[page_id]:
            font_name = c_char_p(char_data.font_name.encode("utf-8"))
            text_handler = pdfium_c.FPDFPageObj_NewTextObj(
                page.pdf.raw, font_name, char_data.font_size
            )
            char_code = ord(char_data.char)
            char_code_c_char = c_ushort(char_code)
            char_ptr = POINTER(c_ushort)(char_code_c_char)
            pdfium_c.FPDFText_SetText(text_handler, char_ptr)
            pdfium_c.FPDFPageObj_Transform(
                text_handler, 1, 0, 0, 1, char_data.left, height - char_data.top
            )
            pdfium_c.FPDFPage_InsertObject(page.raw, text_handler)
        pdfium_c.FPDFPage_GenerateContent(page.raw)


def _compress_pages_with_quality(
    pdf_data: bytes,
    image_quality: int,
) -> List[Tuple[bytes, int, int]]:
    """
    Compresses pages with a specific quality.

    :param pdf_data: The input PDF as bytes.
    :param image_quality: Compression quality.
    :return: List of compressed page buffers.
    """
    pdf_document = pdfium.PdfDocument(pdf_data)
    compressed_pages = []
    for page in pdf_document:
        rasterized_page = _rasterize_page(page, image_quality)
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


def _rasterize_page(  # type: ignore
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


def _collect_images_as_pdf(image_list: List[bytes]) -> pdfium.PdfDocument:  # type: ignore
    """
    Converts a list of JPEG images into pages in a PdfDocument.

    :param image_list: A list of bytes representing JPEG images.
    :return: A PdfDocument handle containing the images as pages.
    """
    out_pdf = pdfium.PdfDocument.new()

    for image_bytes in image_list:
        pdf_image = pdfium.PdfImage.new(out_pdf)
        pdf_image.load_jpeg(io.BytesIO(image_bytes))

        width, height = pdf_image.get_size()
        page = out_pdf.new_page(width, height)
        page.insert_obj(pdf_image)
        page.gen_content()

    return out_pdf
