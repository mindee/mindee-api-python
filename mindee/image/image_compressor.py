from __future__ import annotations

import math
from typing import BinaryIO

from mindee.dependencies.checkers import BERNARD_LEDIT_AVAILABLE
from mindee.dependencies.decorators import requires_bernard_ledit

if BERNARD_LEDIT_AVAILABLE:
    # pylint: disable=import-error
    import bernard_ledit.image as bernard_image
else:
    bernard_image = None  # type: ignore[assignment]  # pylint: disable=invalid-name


@requires_bernard_ledit
def compress_image(
    image_buffer: BinaryIO | bytes,
    quality: int = 85,
    max_width: int | float | None = None,
    max_height: int | float | None = None,
) -> bytes:
    """
    Compresses an image with the given parameters.

    :param image_buffer: Buffer representation of an image, also accepts BinaryIO.
    :param quality: Quality to apply to the image (JPEG compression).
    :param max_width: Maximum bound for the width.
    :param max_height: Maximum bound for the height.
    :return:
    """
    max_width = math.floor(max_width) if max_width else None
    max_height = math.floor(max_height) if max_height else None
    if hasattr(image_buffer, "seek") and hasattr(image_buffer, "read"):
        image_buffer.seek(0)
        raw_bytes: bytes = image_buffer.read()
    else:
        raw_bytes = image_buffer
    return bernard_image.compress(raw_bytes, quality, max_width, max_height)[0]
