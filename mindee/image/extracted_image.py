from __future__ import annotations

from pathlib import Path
from typing import Any, BinaryIO

from mindee.dependencies.checkers import PILLOW_AVAILABLE
from mindee.dependencies.decorators import requires_pillow
from mindee.error.mindee_error import MindeeError
from mindee.input.bytes_input import BytesInput
from mindee.logger import logger

if PILLOW_AVAILABLE:
    # pylint: disable=import-error
    from PIL import Image
else:
    Image: Any = None  # type: ignore[no-redef] # pylint: disable=invalid-name


class ExtractedImage:
    """Generic class for image extraction."""

    buffer: BinaryIO
    filename: str
    _page_id: int
    """Id of the page the image was extracted from."""
    _element_id: int
    """Id of the element on a given page."""

    def __init__(
        self,
        img_byte_stream: BinaryIO,
        filename: str,
        page_id: int,
        element_id: int,
    ) -> None:
        """
        Initialize the ExtractedImage with a buffer and an internal file name.

        :param img_byte_stream: The raw image bytes.
        :param filename: Name of the file.
        :param page_id: ID of the page the element was found on.
        :param element_id: ID of the element in a page.
        """
        self.buffer = img_byte_stream
        self.buffer.seek(0)
        self.filename = filename
        self._page_id = page_id
        self._element_id = 0 if element_id is None else element_id

    @requires_pillow
    def save_to_file(self, output_path: Path | str):
        """
        Saves the document to a file.

        :param output_path: Path to save the file to.
        :raises MindeeError: If an invalid path or filename is provided.
        """
        out_path = Path(output_path)
        if not out_path.resolve().is_dir():
            raise MindeeError("Provided path is not a directory.")
        out_file_path = out_path / self.filename
        try:
            self.buffer.seek(0)
            image = Image.open(self.buffer)
            image.save(out_file_path)
            logger.info("File saved successfully to '%s'.", out_file_path)
        except Exception as e:
            print(e)
            raise MindeeError(f"Could not save file {Path(output_path).name}.") from e

    def as_input_source(self) -> BytesInput:
        """
        Return the file as a Mindee-compatible BufferInput source.

        :returns: A BufferInput source.
        """
        self.buffer.seek(0)
        return BytesInput(self.buffer.read(), self.filename)

    @property
    def page_id(self):
        """
        ID of the page the image was found on.

        :return: A valid page ID.
        """
        return self._page_id

    @property
    def element_id(self):
        """
        ID of the element on a given page.

        :return: A valid element ID.
        """
        return self._element_id
