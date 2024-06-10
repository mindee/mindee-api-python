import io
from typing import BinaryIO, List

import pypdfium2 as pdfium
from PIL import Image

from mindee.geometry import Polygon, get_min_max_x, get_min_max_y


def attach_image_as_new_file(  # type: ignore
    input_buffer: BinaryIO,
) -> pdfium.PdfDocument:
    """
    Attaches an image as a new page in a PdfDocument object.

    :param input_buffer: Input buffer. Only supports JPEG.
    :return: A PdfDocument handle.
    """
    # Create a new page in the PdfDocument
    input_buffer.seek(0)
    image = Image.open(input_buffer)
    image.convert("RGB")
    image_buffer = io.BytesIO()
    image.save(image_buffer, format="JPEG")

    pdf = pdfium.PdfDocument.new()

    image_pdf = pdfium.PdfImage.new(pdf)
    image_pdf.load_jpeg(image_buffer)
    width, height = image_pdf.get_size()

    matrix = pdfium.PdfMatrix().scale(width, height)
    image_pdf.set_matrix(matrix)

    page = pdf.new_page(width, height)
    page.insert_obj(image_pdf)
    page.gen_content()
    image.close()
    return pdf


def extract_from_page(pdf_page: pdfium.PdfPage, polygons: List[Polygon]) -> List[bytes]:  # type: ignore
    """
    Extracts elements from a page based on a list of bounding boxes.

    :param pdf_page: Single PDF Page.
    :param polygons: List of coordinates to pull the elements from.
    :return: List of byte arrays representing the extracted elements.
    """
    width, height = pdf_page.get_size()

    extracted_elements = []
    for polygon in polygons:
        min_max_x = get_min_max_x(polygon)
        min_max_y = get_min_max_y(polygon)

        left = min_max_x.min * width
        right = min_max_x.max * width
        top = min_max_y.min * height
        bottom = min_max_y.max * height

        # Note: cropping done via PIL instead of PyPDFium to simplify operations greatly.
        cropped_content_pil = pdf_page.render().to_pil()
        cropped_content_pil = cropped_content_pil.crop(
            (int(left), int(top), int(right), int(bottom))
        )
        jpeg_buffer = io.BytesIO()
        cropped_content_pil.save(jpeg_buffer, format="PDF")
        jpeg_buffer.seek(0)
        extracted_elements.append(jpeg_buffer.read())

    return extracted_elements
