from __future__ import annotations

import io
from pathlib import Path

from mindee.dependencies import requires_bernard_ledit
from mindee.dependencies.checkers import BERNARD_LEDIT_AVAILABLE
from mindee.geometry.point import Point
from mindee.geometry.polygon import Polygon
from mindee.image.extracted_image import ExtractedImage
from mindee.input.local_input_source import LocalInputSource

if BERNARD_LEDIT_AVAILABLE:
    # pylint: disable=import-error
    import bernard_ledit.image as bernard_image
else:
    bernard_image = None  # type: ignore[assignment]  # pylint: disable=invalid-name


@requires_bernard_ledit
def extract_multiple_images_from_source(
    input_source: LocalInputSource,
    page_id: int,
    polygons: list[Polygon | list[Point]],
) -> list[ExtractedImage]:
    """
    Extract multiple images from a source.
    :param input_source: Source to extract images from.
    :param page_id: Page ID.
    :param polygons: List of polygons to extract.
    :return: List of extracted images.
    """
    stem = Path(input_source.filename).stem
    input_source.file_object.seek(0)
    pts = [[(p.x, p.y) for p in poly] for poly in polygons]
    images = bernard_image.extract_from_polygons(input_source.file_object, page_id, pts)

    extracted = []
    for element_id, img in enumerate(images):
        buf = io.BytesIO()
        img.save(buf)
        fmt = str(img.format).lower() if img.format else "jpeg"
        fmt = fmt if fmt != "jpeg" else "jpg"
        extracted.append(
            ExtractedImage(
                buf,
                f"{stem}_page-{page_id + 1:03d}-item-{element_id + 1:03d}.{fmt}",
                page_id,
                element_id,
            )
        )
    return extracted
