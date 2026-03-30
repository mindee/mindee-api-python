from typing import List

from mindee.error import MindeeError
from mindee.extraction import ExtractedImage, extract_multiple_images_from_source
from mindee.geometry import Polygon
from mindee.input.sources.local_input_source import LocalInputSource
from mindee.parsing.v2.field import FieldLocation
from mindee.v2.product.crop.crop_box import CropBox


class Crop:
    """Crop operations for V2."""

    @classmethod
    def extract_single_crop(
        cls, input_source: LocalInputSource, crop: FieldLocation
    ) -> ExtractedImage:
        """
        Extracts a single crop as complete PDFs from the document.

        :param input_source: Local Input Source to extract sub-receipts from.
        :param crop: Crop to extract.
        :return: ExtractedImage.
        """

        return extract_multiple_images_from_source(
            input_source, crop.page, [crop.polygon]
        )[0]

    @classmethod
    def extract_crops(
        cls, input_source: LocalInputSource, crops: List[CropBox]
    ) -> List[ExtractedImage]:
        """
        Extracts individual receipts from multi-receipts documents.

        :param input_source: Local Input Source to extract sub-receipts from.
        :param crops: List of crops.
        :return: Individual extracted receipts as an array of ExtractedImage.
        """
        images: List[ExtractedImage] = []
        if not crops:
            raise MindeeError("No possible candidates found for Crop extraction.")
        polygons: List[List[Polygon]] = [[] for _ in range(input_source.page_count)]
        for i, crop in enumerate(crops):
            polygons[crop.location.page].append(crop.location.polygon)
        for i, polygon in enumerate(polygons):
            images.extend(
                extract_multiple_images_from_source(
                    input_source,
                    i,
                    polygon,
                )
            )
        return images

    @classmethod
    def apply(
        cls,
        input_source: LocalInputSource,
        crops: List[CropBox],
    ) -> List[ExtractedImage]:
        """Crop a document into multiple pages.

        :param input_source: Input source to crop.
        :param crops: List of crops.
        """

        return cls.extract_crops(input_source, crops)
