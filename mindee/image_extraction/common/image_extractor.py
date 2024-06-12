import io
from typing import BinaryIO, List

import pypdfium2 as pdfium
from PIL import Image

from mindee.geometry import Point, get_min_max_x, get_min_max_y
from mindee.image_extraction.common import ExtractedImage
from mindee.input import BytesInput, LocalInputSource


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


def extract_multiple_images_from_source(
    input_source: LocalInputSource, page_id: int, polygons: List[List[Point]]
) -> List[ExtractedImage]:
    """
    Extracts elements from a page based on a list of bounding boxes.

    :param input_source: Local Input source to extract elements from.
    :param page_id: id of the page to extract from.
    :param polygons: List of coordinates to pull the elements from.
    :return: List of byte arrays representing the extracted elements.
    """
    page = load_pdf_doc(input_source).get_page(page_id)
    page_content = page.render().to_pil()
    width, height = page.get_size()

    extracted_elements = []
    for element_id, polygon in enumerate(polygons):
        min_max_x = get_min_max_x(polygon)
        min_max_y = get_min_max_y(polygon)

        pillow_page = page_content.crop(
            (
                int(min_max_x.min * width),
                int(min_max_y.min * height),
                int(min_max_x.max * width),
                int(min_max_y.max * height),
            )
        )
        buffer = io.BytesIO()
        pillow_page.save(buffer, format="JPEG")
        buffer.seek(0)
        extracted_elements.append(
            ExtractedImage(
                BytesInput(
                    buffer.read(),
                    f"{input_source.filename}_p{page_id}_e{element_id}.jpg",
                ),
                page_id,
                element_id,
            )
        )

    return extracted_elements


def load_pdf_doc(input_file: LocalInputSource) -> pdfium.PdfDocument:  # type: ignore
    """
    Loads a PDF document from a local input source.

    :param input_file: Local input.
    :return: A valid PdfDocument handle.
    """
    if input_file.is_pdf():
        input_file.file_object.seek(0)
        return pdfium.PdfDocument(input_file.file_object)

    return attach_image_as_new_file(input_file.file_object)
