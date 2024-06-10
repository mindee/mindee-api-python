import io
from pathlib import Path
from typing import BinaryIO, List, Union

import pypdfium2 as pdfium
from PIL import Image

from mindee.geometry import Point, get_min_max_x, get_min_max_y


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


def extract_multiple_images_from_image(
    image: Union[bytes, str, Path], polygons: List[List[Point]]
) -> List[Image.Image]:
    """
    Extracts elements from an image based on a list of bounding boxes.

    :param image: Image as a path
    :param polygons: List of coordinates to pull the elements from.
    :return: List of byte arrays representing the extracted elements.
    """
    return extract_multiple_images_from_page(Image.open(image), polygons)


def extract_multiple_images_from_page(  # type: ignore
    page: Union[pdfium.PdfPage, Image.Image], polygons: List[List[Point]]
) -> List[Image.Image]:
    """
    Extracts elements from a page based on a list of bounding boxes.

    :param page: Single PDF Page. If the page is a pdfium.PdfPage, it is rasterized first.
    :param polygons: List of coordinates to pull the elements from.
    :return: List of byte arrays representing the extracted elements.
    """
    if isinstance(page, pdfium.PdfPage):
        page_content = page.render().to_pil()
        width, height = page.get_size()
    else:
        page_content = page
        width, height = page.size

    extracted_elements = []
    for polygon in polygons:
        min_max_x = get_min_max_x(polygon)
        min_max_y = get_min_max_y(polygon)

        left = min_max_x.min * width
        right = min_max_x.max * width
        top = min_max_y.min * height
        bottom = min_max_y.max * height

        extracted_elements.append(
            page_content.crop((int(left), int(top), int(right), int(bottom)))
        )

    return extracted_elements
