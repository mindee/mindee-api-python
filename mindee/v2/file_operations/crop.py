from typing import List, Union

from mindee.error import MindeeError
from mindee.extraction import ExtractedImage, extract_multiple_images_from_source
from mindee.geometry import Point, Polygon
from mindee.input.sources.local_input_source import LocalInputSource
from mindee.parsing.v2.field import FieldLocation
from mindee.v2.file_operations.crop_files import CropFiles
from mindee.v2.product.crop.crop_box import CropBox


def extract_single_crop(
    input_source: LocalInputSource, crop: FieldLocation
) -> ExtractedImage:
    """
    Extracts a single crop as complete PDFs from the document.

    :param input_source: Local Input Source to extract sub-receipts from.
    :param crop: Crop to extract.
    :return: ExtractedImage.
    """

    polygons: List[Union[Polygon, List[Point]]] = [crop.polygon]
    return extract_multiple_images_from_source(input_source, crop.page, polygons)[0]


def extract_crops(input_source: LocalInputSource, crops: List[CropBox]) -> CropFiles:
    """
    Extracts individual receipts from multi-receipts documents.

    :param input_source: Local Input Source to extract sub-receipts from.
    :param crops: List of crops.
    :return: Individual extracted receipts as an array of ExtractedImage.
    """
    images: List[ExtractedImage] = []
    if not crops:
        raise MindeeError("No possible candidates found for Crop extraction.")
    polygons: List[List[Union[Polygon, List[Point]]]] = [
        [] for _ in range(input_source.page_count)
    ]
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
    return CropFiles(images)
