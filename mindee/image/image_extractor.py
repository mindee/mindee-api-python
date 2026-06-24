from __future__ import annotations

import io
from pathlib import Path
from typing import Any, BinaryIO

from mindee.dependencies import requires_pypdfium2
from mindee.dependencies.checkers import PILLOW_AVAILABLE, PYPDFIUM2_AVAILABLE
from mindee.dependencies.decorators import requires_pillow
from mindee.error.mindee_error import MindeeError
from mindee.geometry.point import Point
from mindee.geometry.polygon import Polygon, get_min_max_x, get_min_max_y
from mindee.image.extracted_image import ExtractedImage
from mindee.input.local_input_source import LocalInputSource

if PYPDFIUM2_AVAILABLE:
    # pylint: disable=import-error
    import pypdfium2 as pdfium
else:
    pdfium = None  # pylint: disable=invalid-name


if PILLOW_AVAILABLE:
    # pylint: disable=import-error
    from PIL import Image
else:
    Image: Any = None  # type: ignore[no-redef] # pylint: disable=invalid-name


@requires_pillow
@requires_pypdfium2
def _attach_image_as_new_file(  # type: ignore
    input_buffer: BinaryIO,
) -> pdfium.PdfDocument:
    """
    Attaches an image as a new page in a PdfDocument object.

    :param input_buffer: Input buffer.
    :return: A PdfDocument handle.
    """
    input_buffer.seek(0)
    image = Image.open(input_buffer)
    image.convert("RGB")
    image_buffer = io.BytesIO()
    image.save(image_buffer, format="JPEG")

    pdf = pdfium.PdfDocument.new()

    image_pdf = pdfium.PdfImage.new(pdf)
    image_pdf.load_jpeg(image_buffer)
    width, height = image.width, image.height
    matrix = pdfium.PdfMatrix().scale(width, height)
    image_pdf.set_matrix(matrix)

    page = pdf.new_page(width, height)
    page.insert_obj(image_pdf)
    page.gen_content()
    image.close()
    return pdf


@requires_pillow
def extract_image_from_polygon(
    page_content: Image.Image,
    polygon: list[Point],
    width: float,
    height: float,
    file_format: str,
) -> BinaryIO:
    """
    Crops the image from the given polygon.

    :param page_content: Contents of the page as a Pillow object.
    :param polygon: Polygon coordinates for the image.
    :param width: Width of the generated image.
    :param height: Height of the generated image.
    :param file_format: Format for the generated file.
    :return: A generated image as a buffer.
    """
    min_max_x = get_min_max_x(polygon)
    min_max_y = get_min_max_y(polygon)
    cropped_image = page_content.crop(
        (
            int(min_max_x.min * width),
            int(min_max_y.min * height),
            int(min_max_x.max * width),
            int(min_max_y.max * height),
        )
    )
    return _save_image_to_buffer(cropped_image, file_format)


@requires_pillow
def _save_image_to_buffer(image: Image.Image, file_format: str) -> BinaryIO:
    """
    Saves an image as a buffer.

    :param image: Pillow wrapper for the image.
    :param file_format: Format to save the file as.
    :return: A valid buffer.
    """
    buffer = io.BytesIO()
    image.save(buffer, format=file_format)
    buffer.seek(0)
    return buffer


@requires_pillow
def determine_file_format(input_source: LocalInputSource) -> str:
    """
    Retrieves the file format from an input source.

    :param input_source: Local input source to retrieve the format from.
    :return: A valid pillow file format.
    """
    if input_source.is_pdf():
        return "JPEG"
    img = Image.open(input_source.file_object)
    if img.format is None:
        raise MindeeError("Image format was not found.")
    return img.format


def get_file_extension(file_format: str):
    """
    Extract the correct file extension.

    :param file_format: Format of the file.
    :return: A valid file extension.
    """
    return file_format.lower() if file_format != "JPEG" else "jpg"


@requires_pillow
def extract_multiple_images_from_source(
    input_source: LocalInputSource,
    page_id: int,
    polygons: list[Polygon | list[Point]],
) -> list[ExtractedImage]:
    """
    Extracts elements from a page based on a list of bounding boxes.

    :param input_source: Local Input source to extract elements from.
    :param page_id: id of the page to extract from.
    :param polygons: List of coordinates to pull the elements from.
    :return: List of byte arrays representing the extracted elements.
    """
    stem = Path(input_source.filename).stem
    page = _load_pdf_doc(input_source).get_page(page_id)
    page_content = page.render().to_pil()
    width, height = page.get_size()

    file_format = determine_file_format(input_source)
    file_extension = get_file_extension(file_format)

    extracted_elements = []
    for element_id, polygon in enumerate(polygons):
        image_data = extract_image_from_polygon(
            page_content, polygon, width, height, file_format
        )
        extracted_elements.append(
            ExtractedImage(
                image_data,
                f"{stem}_page-{(page_id + 1):03d}-item-{(element_id + 1):03d}.{file_extension}",
                page_id,
                element_id,
            )
        )
    return extracted_elements


@requires_pypdfium2
def _load_pdf_doc(input_file: LocalInputSource) -> pdfium.PdfDocument:  # type: ignore
    """
    Loads a PDF document from a local input source.

    :param input_file: Local input.
    :return: A valid PdfDocument handle.
    """
    if input_file.is_pdf():
        input_file.file_object.seek(0)
        return pdfium.PdfDocument(input_file.file_object.read())

    return _attach_image_as_new_file(input_file.file_object)
