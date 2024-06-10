from typing import List, Union

import pypdfium2 as pdfium

from mindee.error import MimeTypeError, MindeeError
from mindee.geometry.point import Point
from mindee.geometry.polygon import Polygon
from mindee.geometry.quadrilateral import Quadrilateral
from mindee.image_extraction.common.image_extractor import (
    attach_image_as_new_file,
    extract_from_page,
)
from mindee.image_extraction.multi_receipts_extractor.extracted_multi_receipt_image import (
    ExtractedMultiReceiptsImage,
)
from mindee.input import LocalInputSource
from mindee.parsing.common import Inference


def extract_receipts_from_page(  # type: ignore
    pdf_page: pdfium.PdfPage,
    bounding_boxes: List[Union[List[Point], Polygon, Quadrilateral]],
    page_id: int,
) -> List[ExtractedMultiReceiptsImage]:
    """
    Given a page and a set of coordinates, extracts & assigns individual receipts to an ExtractedMultiReceiptsImage\
    object.

    :param pdf_page: PDF Page to extract from.
    :param bounding_boxes: A set of coordinates delimiting the position of each receipt.
    :param page_id: ID of the page the receipt is extracted from. Caution: this starts at 0, unlike the numbering in PDF
    pages.
    :return: A list of ExtractedMultiReceiptsImage.
    """
    extracted_receipts_raw = extract_from_page(pdf_page, bounding_boxes)  # type: ignore
    extracted_receipts = []
    for i, extracted_receipt_raw in enumerate(extracted_receipts_raw):
        extracted_receipts.append(
            ExtractedMultiReceiptsImage(extracted_receipt_raw, i, page_id)
        )
    return extracted_receipts


def load_pdf_doc(input_file: LocalInputSource) -> pdfium.PdfDocument:  # type: ignore
    """
    Loads a PDF document from a local input source.

    :param input_file: Local input.
    :return: A valid PdfDocument handle.
    """
    if input_file.file_mimetype not in [
        "application/pdf",
        "image/heic",
        "image/png",
        "image/jpg",
        "image/jpeg",
        "image/tiff",
        "image/webp",
    ]:
        raise MimeTypeError(f"Unsupported file type '{input_file.file_mimetype}'.")
    input_file.file_object.seek(0)
    if input_file.is_pdf():
        return pdfium.PdfDocument(input_file.file_object)

    return attach_image_as_new_file(input_file.file_object)


def extract_receipts(
    input_file: LocalInputSource, inference: Inference
) -> List[ExtractedMultiReceiptsImage]:
    """
    Extracts individual receipts from multi-receipts documents.

    :param input_file: File to extract sub-receipts from.
    :param inference: Results of the inference.
    :return: Individual extracted receipts as an array of ExtractedMultiReceiptsImage.
    """
    images: List[ExtractedMultiReceiptsImage] = []
    if not inference.prediction.receipts:
        raise MindeeError(
            "No possible receipts candidates found for MultiReceipts extraction."
        )
    pdf_doc = load_pdf_doc(input_file)
    for page_id, page in enumerate(pdf_doc):
        receipt_positions = [
            receipt.bounding_box
            for receipt in inference.pages[page_id].prediction.receipts
        ]
        extracted_receipts = extract_receipts_from_page(
            page, receipt_positions, page_id
        )
        images.extend(extracted_receipts)
    return images
