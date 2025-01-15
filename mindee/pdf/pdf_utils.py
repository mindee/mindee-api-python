from ctypes import byref, c_double, c_int, create_string_buffer
from threading import RLock
from typing import List, Tuple

import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c

from mindee.pdf.pdf_char_data import PDFCharData

FALLBACK_FONT = "Helvetica"


def has_source_text(pdf_bytes: bytes) -> bool:
    """
    Checks if the provided PDF bytes contain source text.

    :param pdf_bytes: Raw bytes representation of a PDF file
    :return:
    """
    pdf = pdfium.PdfDocument(pdf_bytes)
    for page in pdf:
        if len(page.get_textpage().get_text_bounded().strip()) > 0:
            return True
    return False


def extract_text_from_pdf(pdf_bytes: bytes) -> List[PDFCharData]:
    """
    Extracts the raw text from a given PDF's bytes along with font data.

    :param pdf_bytes: Raw bytes representation of a PDF file.
    :return: A list of info regarding each read character.
    """
    char_data_list: List[PDFCharData] = []
    pdfium_lock = RLock()
    pdf = pdfium.PdfDocument(pdf_bytes)

    for page in pdf:
        process_page(page, pdfium_lock, char_data_list)

    return char_data_list


def process_page(page, pdfium_lock: RLock, char_data_list: List[PDFCharData]):
    """
    Processes a single page of the PDF.

    :param page: The PDF page to process.
    :param pdfium_lock: Lock for thread-safe operations.
    :param char_data_list: List to append character data to.
    """
    internal_height = page.get_height()
    internal_width = page.get_width()

    with pdfium_lock:
        text_handler = pdfium_c.FPDFText_LoadPage(page.raw)
        count_chars = pdfium_c.FPDFText_CountChars(text_handler)

    for i in range(count_chars):
        process_char(
            i,
            text_handler,
            page,
            pdfium_lock,
            internal_height,
            internal_width,
            char_data_list,
        )

    with pdfium_lock:
        pdfium_c.FPDFText_ClosePage(text_handler)


def process_char(
    i: int,
    text_handler,
    page,
    pdfium_lock: RLock,
    internal_height: float,
    internal_width: float,
    char_data_list: List[PDFCharData],
):
    """
    Processes a single character from the PDF.

    :param i: The index of the character.
    :param text_handler: The text handler for the current page.
    :param page: The current page being processed.
    :param pdfium_lock: Lock for thread-safe operations.
    :param internal_height: The height of the page.
    :param internal_width: The width of the page.
    :param char_data_list: List to append character data to.
    """
    char_info = get_char_info(i, text_handler, pdfium_lock)
    char_box = get_char_box(i, text_handler, pdfium_lock)
    rotation = get_page_rotation(page, pdfium_lock)

    adjusted_box = adjust_char_box(char_box, rotation, internal_height, internal_width)

    for c in char_info["char"] or " ":
        char_data = PDFCharData(
            char=c,
            left=int(adjusted_box[0]),
            right=int(adjusted_box[1]),
            top=int(adjusted_box[2]),
            bottom=int(adjusted_box[3]),
            font_name=char_info["font_name"],
            font_size=char_info["font_size"],
            font_weight=char_info["font_weight"],
            font_stroke_color=char_info["font_stroke_color"],
            font_fill_color=char_info["font_fill_color"],
            font_flags=char_info["font_flags"],
        )
        char_data_list.append(char_data)


def get_char_info(i: int, text_handler, pdfium_lock: RLock) -> dict:
    """
    Retrieves information about a specific character.

    :param i: The index of the character.
    :param text_handler: The text handler for the current page.
    :param pdfium_lock: Lock for thread-safe operations.
    :return: A dictionary containing character information.
    """
    with pdfium_lock:
        char = chr(pdfium_c.FPDFText_GetUnicode(text_handler, i))
        font_name = get_font_name(text_handler, i)
        font_flags = get_font_flags(text_handler, i)
        font_size = pdfium_c.FPDFText_GetFontSize(text_handler, i)
        font_weight = pdfium_c.FPDFText_GetFontWeight(text_handler, i)
        font_stroke_color = pdfium_c.FPDFText_GetStrokeColor(text_handler, i)
        font_fill_color = pdfium_c.FPDFText_GetFillColor(text_handler, i)

    return {
        "char": char,
        "font_name": font_name,
        "font_flags": font_flags,
        "font_size": font_size,
        "font_weight": font_weight,
        "font_stroke_color": font_stroke_color,
        "font_fill_color": font_fill_color,
    }


def get_font_name(text_handler, i: int) -> str:
    """
    Retrieves the font name for a specific character.

    :param text_handler: The text handler for the current page.
    :param i: The index of the character.
    :return: The font name as a string.
    """
    buffer_length = 128
    font_name_buffer = create_string_buffer(buffer_length)
    flags = c_int(0)
    actual_length = pdfium_c.FPDFText_GetFontInfo(
        text_handler, i, font_name_buffer, buffer_length, byref(flags)
    )
    return (
        font_name_buffer.value.decode("utf-8") if actual_length > 0 else FALLBACK_FONT
    )


def get_font_flags(text_handler, i: int) -> int:
    """
    Retrieves the font flags for a specific character.

    :param text_handler: The text handler for the current page.
    :param i: The index of the character.
    :return: The font flags as an integer.
    """
    flags = c_int(0)
    pdfium_c.FPDFText_GetFontInfo(text_handler, i, None, 0, byref(flags))
    return flags.value


def get_char_box(
    i: int, text_handler, pdfium_lock: RLock
) -> Tuple[float, float, float, float]:
    """
    Retrieves the bounding box for a specific character.

    :param i: The index of the character.
    :param text_handler: The text handler for the current page.
    :param pdfium_lock: Lock for thread-safe operations.
    :return: A tuple containing left, right, bottom, and top coordinates.
    """
    left, right, bottom, top = (c_double(0), c_double(0), c_double(0), c_double(0))
    with pdfium_lock:
        pdfium_c.FPDFText_GetCharBox(
            text_handler, i, byref(left), byref(right), byref(bottom), byref(top)
        )
    return left.value, right.value, bottom.value, top.value


def get_page_rotation(page, pdfium_lock: RLock) -> int:
    """
    Retrieves the rotation value for a specific page.

    :param page: The page to get the rotation for.
    :param pdfium_lock: Lock for thread-safe operations.
    :return: The rotation value in degrees.
    """
    with pdfium_lock:
        return {0: 0, 1: 90, 2: 180, 3: 270}.get(
            pdfium_c.FPDFPage_GetRotation(page.raw), 0
        )


def adjust_char_box(
    char_box: Tuple[float, float, float, float],
    rotation: int,
    internal_height: float,
    internal_width: float,
) -> Tuple[float, float, float, float]:
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
