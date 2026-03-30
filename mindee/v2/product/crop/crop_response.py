from typing import List

from mindee.error import MindeeError
from mindee.extraction.common.extracted_image import ExtractedImage
from mindee.extraction.common.image_extractor import extract_multiple_images_from_source
from mindee.geometry import Polygon
from mindee.input.sources.local_input_source import LocalInputSource
from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference import BaseResponse
from mindee.v2.product.crop.crop_inference import CropInference


class CropResponse(BaseResponse):
    """Represent a crop inference response from Mindee V2 API."""

    inference: CropInference
    """Inference object for crop inference."""

    _slug: str = "products/crop/results"
    """Slug of the inference."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.inference = CropInference(raw_response["inference"])

    def apply_to_file(self, input_source: LocalInputSource) -> List[ExtractedImage]:
        """
        Apply the crop inference to a file and return a list of extracted images.

        :param input_source: Local file to apply the inference to
        :return: List of extracted PDFs
        """
        crops = self.inference.result.crops
        if not crops:
            raise MindeeError("No possible candidates found for Crop extraction.")

        polygons: List[List[Polygon]] = [[] for _ in range(input_source.page_count)]
        for crop in crops:
            polygons[crop.location.page].append(crop.location.polygon)

        images: List[ExtractedImage] = []
        for page_index, page_polygons in enumerate(polygons):
            if not page_polygons:
                continue
            images.extend(
                extract_multiple_images_from_source(
                    input_source,
                    page_index,
                    page_polygons,
                )
            )
        return images
