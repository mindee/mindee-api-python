from typing import List, Union

import pypdfium2 as pdfium

from mindee.error import MimeTypeError, MindeeError
from mindee.geometry.point import Point
from mindee.geometry.polygon import Polygon
from mindee.geometry.quadrilateral import Quadrilateral
from mindee.image_extraction.common.image_extractor import (
    attach_bitmap_as_new_page,
    extract_from_page,
    get_image_size,
)
from mindee.image_extraction.multi_receipts_extractor.extracted_multi_receipt_image import (
    ExtractedMultiReceiptImage,
)
from mindee.input import LocalInputSource
from mindee.product import MultiReceiptsDetectorV1


def extract_receipts_from_page(  # type: ignore
    pdf_page: pdfium.PdfPage,
    bounding_boxes: List[Union[List[Point], Polygon, Quadrilateral]],
    page_id: int,
) -> List[ExtractedMultiReceiptImage]:
    """
    Given a page and a set of coordinates, extracts & assigns individual receipts to an ExtractedMultiReceiptImage\
    object.

    :param pdf_page: PDF Page to extract from.
    :param bounding_boxes: A set of coordinates delimiting the position of each receipt.
    :param page_id: ID of the page the receipt is extracted from. Caution: this starts at 0, unlike the numbering in PDF
    pages.
    :return: A list of ExtractedMultiReceiptImage.
    """
    extracted_receipts_raw = extract_from_page(pdf_page, bounding_boxes)  # type: ignore
    extracted_receipts = []
    for i, extracted_receipt_raw in enumerate(extracted_receipts_raw):
        extracted_receipts.append(
            ExtractedMultiReceiptImage(extracted_receipt_raw, i, page_id)
        )
    return extracted_receipts


def load_pdf_doc(input_file: LocalInputSource) -> pdfium.PdfDocument:  # type: ignore
    """
    Loads a PDF document from a local input source.

    :param input_file: Local input.
    :return: A valid PdfDocument handle.
    """
    if input_file.file_mimetype not in [
        "image/jpeg",
        "image/jpg",
        "image/png",
        "application/pdf",
    ]:
        raise MimeTypeError(
            f"Unsupported file type '{input_file.file_mimetype}'. Currently supported types are '.png',"
            f" '.jpg' and '.pdf'."
        )
    if input_file.is_pdf():
        return pdfium.PdfDocument(input_file.file_object)
    pdf_document = pdfium.PdfDocument.new()
    height, width = get_image_size(input_file.file_object)
    pdf_bitmap = pdfium.PdfBitmap.new_native(width, height, 4)
    pdf_bitmap = pdfium.PdfBitmap(
        raw=pdf_bitmap,
        buffer=input_file.file_object,
        height=height,
        width=width,
        needs_free=True,
        rev_byteorder=False,
        format=4,
        stride=4,
    )
    # Bitmap format 4 should equate to RGBA, assumed to be equivalent to:
    # https://docs.rs/pdfium-render/latest/pdfium_render/bitmap/enum.PdfBitmapFormat.html

    return attach_bitmap_as_new_page(pdf_document, pdf_bitmap, height, width)


def extract_receipts(
    input_file: LocalInputSource, inference: MultiReceiptsDetectorV1
) -> List[ExtractedMultiReceiptImage]:
    """
    Extracts individual receipts from multi-receipts documents.

    :param input_file: File to extract sub-receipts from.
    :param inference: Results of the inference.
    :return: Individual extracted receipts as an array of ExtractedMultiReceiptImage.
    """
    images: List[ExtractedMultiReceiptImage] = []
    if not inference.prediction.receipts:
        raise MindeeError(
            "No possible receipts candidates found for MultiReceipts extraction."
        )
    pdf_doc = load_pdf_doc(input_file)
    for page_id in range(len(pdf_doc)):
        receipt_positions = [
            receipt.bounding_box
            for receipt in inference.pages[page_id].prediction.receipts
        ]
        extracted_receipts = extract_receipts_from_page(
            pdf_doc.get_page(page_id), receipt_positions, page_id  # type: ignore
        )
        images.extend(extracted_receipts)
    return images
