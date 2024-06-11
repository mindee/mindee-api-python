import io
from typing import List

from mindee.error import MindeeError
from mindee.image_extraction.common.image_extractor import (
    extract_multiple_images_from_page,
    load_pdf_doc,
)
from mindee.image_extraction.multi_receipts_extractor.extracted_multi_receipt_image import (
    ExtractedMultiReceiptsImage,
)
from mindee.input import LocalInputSource
from mindee.parsing.common import Inference


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
        extracted_receipts = []
        receipts = extract_multiple_images_from_page(page, receipt_positions)
        for receipt_id, receipt in enumerate(receipts):
            buffer = io.BytesIO()
            receipt.save(buffer, format="JPEG")
            buffer.seek(0)
            extracted_receipts.append(
                ExtractedMultiReceiptsImage(buffer.read(), receipt_id, page_id)
            )
        images.extend(extracted_receipts)
    return images
