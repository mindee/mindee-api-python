from __future__ import annotations

import io
from typing import Any, BinaryIO

from mindee.dependencies.checkers import PILLOW_AVAILABLE
from mindee.dependencies.decorators import requires_pillow

if PILLOW_AVAILABLE:
    # pylint: disable=import-error
    from PIL import Image
else:
    Image: Any = None  # type: ignore[no-redef] # pylint: disable=invalid-name


@requires_pillow
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
    if isinstance(image_buffer, bytes):
        image_buffer = io.BytesIO(image_buffer)
    with Image.open(image_buffer) as img:
        original_width, original_height = img.size
        max_width = max_width or original_width
        max_height = max_height or original_height
        if max_width or max_height:
            img.thumbnail((int(max_width), int(max_height)), Image.Resampling.LANCZOS)

        output_buffer = io.BytesIO()
        img.save(output_buffer, format="JPEG", quality=quality, optimize=True)

        compressed_image = output_buffer.getvalue()
    return compressed_image
