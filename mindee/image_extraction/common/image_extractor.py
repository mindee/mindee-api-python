import io
from typing import List, BinaryIO, Tuple

import pypdfium2 as pdfium

from mindee.error import MimeTypeError
from mindee.geometry import get_min_max_x, get_min_max_y, Polygon

import struct


def get_image_size(data: BinaryIO) -> Tuple[int, int]:
    """
    Read the first few bytes to determine the file type.

    :param data: Image input.
    :return: A tuple containing the file's height/width.
    """
    data.seek(0)
    signature = data.read(8)

    # Check for PNG signature
    if signature[:8] == b'\x89PNG\r\n\x1a\n':
        # PNG file
        data.seek(16)
        width, height = struct.unpack('>II', data.read(8))
        return width, height

    # Check for JPEG SOI marker
    elif signature[:2] == b'\xff\xd8':
        data.seek(2)
        while True:
            marker, = struct.unpack('>H', data.read(2))
            if marker == 0xFFC0 or marker == 0xFFC2:  # SOF0 or SOF2
                data.seek(3, 1)  # Skip length and precision
                height, width = struct.unpack('>HH', data.read(4))
                return width, height
            else:
                length, = struct.unpack('>H', data.read(2))
                data.seek(length - 2, 1)
    data.close()
    raise MimeTypeError("Size could not be retrieved for file.")


def attach_bitmap_as_new_page(pdf_doc: pdfium.PdfDocument, bitmap: pdfium.PdfBitmap, new_width: float,
                              new_height: float) -> pdfium.PdfDocument:
    """
    Attaches a created PdfBitmap object as a new page in a PdfDocument object.

    :param pdf_doc: The PdfDocument to which the new page will be added.
    :param bitmap: The PdfBitmap object to be added as a new page.
    :param new_width: The width of the new page.
    :param new_height: The height of the new page.
    """
    # Create a new page in the PdfDocument
    new_page = pdf_doc.new_page(new_width, new_height)

    # Create a device context to render the bitmap onto the new page
    new_page.insert_obj(bitmap.buffer)

    return pdf_doc


def extract_from_page(pdf_page: pdfium.PdfPage, polygons: List[Polygon]):
    """
    Extracts elements from a page based on a list of bounding boxes.

    :param pdf_page: Single PDF Page.
    :param polygons: List of coordinates to pull the elements from.
    :return: List of byte arrays representing the extracted elements.
    """
    width, height = pdf_page.get_size()

    extracted_elements = []

    for polygon in polygons:
        temp_pdf = pdfium.PdfDocument.new()

        min_max_x = get_min_max_x(polygon)
        min_max_y = get_min_max_y(polygon)

        new_width = width * (min_max_x.max - min_max_x.min)
        new_height = height * (min_max_y.max - min_max_y.min)

        left = min_max_x.min * width
        right = min_max_x.max * width
        top = height - (min_max_y.min * height)
        bottom = height - (min_max_y.max * height)

        cropped_page: pdfium.PdfBitmap = pdf_page.render(crop=(left, bottom, right, top))

        temp_pdf = attach_bitmap_as_new_page(temp_pdf, cropped_page, new_width, new_height)

        temp_file = io.BytesIO()
        temp_pdf.save(temp_file)
        extracted_elements.append(temp_file.read())
        temp_file.close()

    return extracted_elements
