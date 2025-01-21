import ctypes
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


def extract_text_from_pdf(pdf_bytes: bytes) -> List[List[PDFCharData]]:
    """
    Extracts the raw text from a given PDF's bytes along with font data.

    :param pdf_bytes: Raw bytes representation of a PDF file.
    :return: A list of info regarding each read character.
    """
    pdfium_lock = RLock()
    pdf = pdfium.PdfDocument(pdf_bytes)
    char_data_list: List[List[PDFCharData]] = []

    for i, page in enumerate(pdf):
        char_data_list.append(_process_page(page, i, pdfium_lock))

    return char_data_list


def _process_page(page, page_id: int, pdfium_lock: RLock) -> List[PDFCharData]:
    """
    Processes a single page of the PDF.

    :param page: The PDF page to process.
    :param page_id: ID of the page.
    :param pdfium_lock: Lock for thread-safe operations.
    """
    char_data_list: List[PDFCharData] = []
    internal_height = page.get_height()
    internal_width = page.get_width()

    with pdfium_lock:
        text_handler = pdfium_c.FPDFText_LoadPage(page.raw)
        count_chars = pdfium_c.FPDFText_CountChars(text_handler)

    for i in range(count_chars):
        concatenated_chars = _process_char(
            i, text_handler, page, pdfium_lock, internal_height, internal_width, page_id
        )
        for concatenated_char in concatenated_chars:
            char_data_list.append(concatenated_char)

    with pdfium_lock:
        pdfium_c.FPDFText_ClosePage(text_handler)
    return char_data_list


def _process_char(
    i: int,
    text_handler,
    page,
    pdfium_lock: RLock,
    internal_height: float,
    internal_width: float,
    page_id: int,
) -> List[PDFCharData]:
    """
    Processes a single character from the PDF.

    :param i: The index of the character.
    :param text_handler: The text handler for the current page.
    :param page: The current page being processed.
    :param pdfium_lock: Lock for thread-safe operations.
    :param internal_height: The height of the page.
    :param internal_width: The width of the page.
    :param page_id: ID of the page the character was found on.
    :return: List of character data for a page.
    """
    char_info = _get_char_info(i, text_handler, pdfium_lock)
    if not char_info:
        return []
    char_box = _get_char_box(i, text_handler, pdfium_lock)
    rotation = _get_page_rotation(page, pdfium_lock)

    adjusted_box = _adjust_char_box(char_box, rotation, internal_height, internal_width)
    char_data_list: List[PDFCharData] = []
    for c in char_info["char"] or " ":
        if c in (
            "\n",
            "\r",
        ):  # Removes duplicated carriage returns in the PDF due to weird extraction.
            # IDK how to make this better, and neither does Claude, GPT4 nor GPT-o1, so I'm leaving this weird check.
            next_char_info = _get_char_info(i + 1, text_handler, pdfium_lock)
            if not next_char_info or next_char_info["char"] in ("\n", "\r"):
                continue

        char_data_list.append(
            PDFCharData(
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
                page_id=page_id,
            )
        )
    return char_data_list


def _get_char_info(i: int, text_handler, pdfium_lock: RLock) -> dict:
    """
    Retrieves information about a specific character.

    :param i: The index of the character.
    :param text_handler: The text handler for the current page.
    :param pdfium_lock: Lock for thread-safe operations.
    :return: A dictionary containing character information.
    """
    stroke = (ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint())
    fill = (ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint())

    with pdfium_lock:
        unicode_char = pdfium_c.FPDFText_GetUnicode(text_handler, i)
        if unicode_char == 0xFF:
            return {}
        char = chr(unicode_char)
        font_name = _get_font_name(text_handler, i)
        font_flags = _get_font_flags(text_handler, i)
        font_size = pdfium_c.FPDFText_GetFontSize(text_handler, i)
        font_weight = pdfium_c.FPDFText_GetFontWeight(text_handler, i)
        _ = pdfium_c.FPDFText_GetStrokeColor(
            text_handler, i, stroke[0], stroke[1], stroke[2], stroke[3]
        )
        _ = pdfium_c.FPDFText_GetFillColor(
            text_handler, i, fill[0], fill[1], fill[2], fill[3]
        )

    return {
        "char": char,
        "font_name": font_name,
        "font_flags": font_flags,
        "font_size": font_size,
        "font_weight": font_weight,
        "font_stroke_color": stroke,
        "font_fill_color": fill,
    }


def _get_font_name(text_handler, i: int) -> str:
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


def _get_font_flags(text_handler, i: int) -> int:
    """
    Retrieves the font flags for a specific character.

    :param text_handler: The text handler for the current page.
    :param i: The index of the character.
    :return: The font flags as an integer.
    """
    flags = c_int(0)
    pdfium_c.FPDFText_GetFontInfo(text_handler, i, None, 0, byref(flags))
    return flags.value


def _get_char_box(
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


def _get_page_rotation(page, pdfium_lock: RLock) -> int:
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


def _adjust_char_box(
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


def lerp(start: float, end: float, t: float) -> float:
    """
    Performs linear interpolation between two numbers.

    :param start: The starting value.
    :param end: The ending value.
    :param t: The interpolation factor (0 to 1).
    :return: The interpolated value.
    """
    return start * (1 - t) + end * t
