from __future__ import annotations

import io
from pathlib import Path
from typing import BinaryIO

from mindee.dependencies import requires_bernard_ledit
from mindee.dependencies.checkers import BERNARD_LEDIT_AVAILABLE
from mindee.geometry.point import Point
from mindee.geometry.polygon import Polygon, get_min_max_x, get_min_max_y
from mindee.image.extracted_image import ExtractedImage
from mindee.input.local_input_source import LocalInputSource

if BERNARD_LEDIT_AVAILABLE:
    # pylint: disable=import-error
    import bernard_ledit.image as bernard_image
    import bernard_ledit.pdf as bernard_pdf
else:
    bernard_pdf = None  # type: ignore[assignment]  # pylint: disable=invalid-name
    bernard_image = None  # type: ignore[assignment]  # pylint: disable=invalid-name


@requires_bernard_ledit
def _attach_image_as_new_file(
    input_buffer: BinaryIO,
) -> bernard_pdf.PdfDocument:
    """
    Attaches an image as a new page in a PdfDocument object.

    :param input_buffer: Input buffer.
    :return: A PdfDocument handle.
    """
    input_buffer.seek(0)
    pdf = bernard_pdf.PdfDocument.new()
    pdf.append_jpeg_page(input_buffer.read())
    return pdf


@requires_bernard_ledit
def extract_image_from_polygon(
    page_content: bernard_image.Image,
    polygon: list[Point],
    width: float,
    height: float,
    file_format: str,
    quality: int = 70,
) -> BinaryIO:
    """
    Crops the image from the given polygon.

    :param page_content: Contents of the page as a Bernard L'Édit Image object.
    :param polygon: Polygon coordinates for the image.
    :param width: Width of the generated image.
    :param height: Height of the generated image.
    :param file_format: Format for the generated file.
    :param quality: JPEG quality for the output (default 70 — sufficient for OCR).
    :return: A generated image as a buffer.
    """
    min_max_x = get_min_max_x(polygon)
    min_max_y = get_min_max_y(polygon)
    cropped_image = page_content.crop(
        left=int(min_max_x.min * width),
        top=int(min_max_y.min * height),
        right=int(min_max_x.max * width),
        bottom=int(min_max_y.max * height),
    )
    return _save_image_to_buffer(cropped_image, file_format, quality)


@requires_bernard_ledit
def _save_image_to_buffer(
    image: bernard_image.Image, file_format: str, quality: int = 70
) -> BinaryIO:
    """
    Saves an image as a buffer.

    :param image: Bernard L'Édit wrapper for the image.
    :param file_format: Format to save the file as.
    :param quality: JPEG quality (default 70 — sufficient for OCR).
    :return: A valid buffer.
    """
    buffer = io.BytesIO()
    image.save(buffer, format=file_format, quality=quality)
    buffer.seek(0)
    return buffer


def get_file_extension(file_format: str):
    """
    Extract the correct file extension.

    :param file_format: Format of the file.
    :return: A valid file extension.
    """
    return file_format.lower() if file_format != "JPEG" else "jpg"


@requires_bernard_ledit
def extract_multiple_images_from_source(
    input_source: LocalInputSource,
    page_id: int,
    polygons: list[Polygon | list[Point]],
    quality: int = 70,
) -> list[ExtractedImage]:
    """
    Extracts elements from a page based on a list of bounding boxes.

    :param input_source: Local Input source to extract elements from.
    :param page_id: id of the page to extract from.
    :param polygons: List of coordinates to pull the elements from.
    :param quality: JPEG quality for extracted images (default 70).
    :return: List of byte arrays representing the extracted elements.
    """
    stem = Path(input_source.filename).stem
    doc = _load_pdf_doc(input_source)
    page_content = doc.rasterize_page(page_id, 100)
    width = doc.get_page(page_id).get_size().width
    height = doc.get_page(page_id).get_size().height

    if input_source.is_pdf():
        file_format = "JPEG"
    else:
        input_source.file_object.seek(0)
        file_format = bernard_image.guess_format(input_source.file_object)

    extracted_elements = []
    decoded_page = bernard_image.decode(page_content)
    for element_id, polygon in enumerate(polygons):
        image_data = extract_image_from_polygon(
            decoded_page,
            polygon,
            width,
            height,
            file_format,
            quality,
        )
        extracted_elements.append(
            ExtractedImage(
                image_data,
                f"{stem}_page-{(page_id + 1):03d}-item-{(element_id + 1):03d}."
                f"{get_file_extension(file_format)}",
                page_id,
                element_id,
            )
        )
    return extracted_elements


@requires_bernard_ledit
def _load_pdf_doc(input_file: LocalInputSource) -> bernard_pdf.PdfDocument:
    """
    Loads a PDF document from a local input source.

    :param input_file: Local input.
    :return: A valid PdfDocument handle.
    """
    if input_file.is_pdf():
        input_file.file_object.seek(0)
        return bernard_pdf.PdfDocument(input_file.file_object.read())

    return _attach_image_as_new_file(input_file.file_object)
