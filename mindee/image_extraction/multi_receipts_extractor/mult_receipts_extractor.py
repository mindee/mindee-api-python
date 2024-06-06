from typing import List

import pypdfium2 as pdfium

from mindee.error import MimeTypeError
from mindee.geometry import Polygon
from mindee.image_extraction.common.image_extractor import extract_from_page, attach_bitmap_as_new_page, get_image_size
from mindee.image_extraction.multi_receipts_extractor import ExtractedMultiReceiptImage
from mindee.input import LocalInputSource


def extract_receipts_from_page(pdf_page: pdfium.PdfPage, bounding_boxes: List[Polygon], page_id: int) \
        -> List[ExtractedMultiReceiptImage]:
    """
    Given a page and a set of coordinates, extracts & assigns individual receipts to an ExtractedMultiReceiptImage
    object.

    :param pdf_page: PDF Page to extract from.
    :param bounding_boxes: A set of coordinates delimiting the position of each receipt.
    :param page_id: ID of the page the receipt is extracted from. Caution: this starts at 0, unlike the numbering in PDF
    pages.
    :return: A list of ExtractedMultiReceiptImage.
    """
    extracted_receipts_raw = extract_from_page(pdf_page, bounding_boxes)
    extracted_receipts = []
    for i in range(len(extracted_receipts_raw)):
        extracted_receipts.append(ExtractedMultiReceiptImage(extracted_receipts_raw[i], page_id, i))
    return extracted_receipts


def load_pdf_doc(input_file: LocalInputSource) -> pdfium.PdfDocument:
    """
    Loads a PDF document from a local input source.

    :param input_file: Local input.
    :return: A valid PdfDocument handle.
    """
    if input_file.file_mimetype not in ["image/jpeg", "image/jpg", "image/png", "application/pdf"]:
        raise MimeTypeError(f"Unsupported file type '{input_file.file_mimetype}'. Currently supported types are '.png',"
                            f" '.jpg' and '.pdf'.")
    if input_file.is_pdf():
        pdf_document = pdfium.PdfDocument(input_file.file_object)
    else:
        pdf_document = pdfium.PdfDocument.new()

    return attach_bitmap_as_new_page(pdf_document, input_file.file_object, get_image_size(input_file.file_object))
