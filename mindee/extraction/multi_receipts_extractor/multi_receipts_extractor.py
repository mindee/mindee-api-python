from typing import List

from mindee.error.mindee_error import MindeeError
from mindee.extraction.common.extracted_image import ExtractedImage
from mindee.extraction.common.image_extractor import (
    extract_multiple_images_from_source,
)
from mindee.input.sources.local_input_source import LocalInputSource
from mindee.parsing.common.inference import Inference


def extract_receipts(
    input_source: LocalInputSource, inference: Inference
) -> List[ExtractedImage]:
    """
    Extracts individual receipts from multi-receipts documents.

    :param input_source: Local Input Source to extract sub-receipts from.
    :param inference: Results of the inference.
    :return: Individual extracted receipts as an array of ExtractedMultiReceiptsImage.
    """
    images: List[ExtractedImage] = []
    if not inference.prediction.receipts:
        raise MindeeError(
            "No possible receipts candidates found for MultiReceipts extraction."
        )
    for page_id in range(input_source.count_doc_pages()):
        receipt_positions = [
            receipt.bounding_box
            for receipt in inference.pages[page_id].prediction.receipts
        ]
        images.extend(
            extract_multiple_images_from_source(
                input_source, page_id, receipt_positions
            )
        )
    return images
