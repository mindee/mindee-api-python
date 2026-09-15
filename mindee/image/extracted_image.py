from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

from mindee.dependencies.checkers import BERNARD_LEDIT_AVAILABLE
from mindee.dependencies.decorators import requires_bernard_ledit
from mindee.error.mindee_error import MindeeError
from mindee.input.bytes_input import BytesInput
from mindee.logger import logger

if BERNARD_LEDIT_AVAILABLE:
    # pylint: disable=import-error
    import bernard_ledit.image as bernard_image
else:
    bernard_image = None  # type: ignore[assignment]  # pylint: disable=invalid-name


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

    @requires_bernard_ledit
    def write_to_file(self, output_path: Path | str, file_format: str | None = None):
        """
        Saves the document to a file.

        When no format conversion is requested the buffer is written directly
        to avoid a lossy decode → re-encode cycle.

        :param output_path: Path to save the file to.
        :param file_format: Format of the file to save. If omitted the buffer is
            written as-is; pass an explicit format to force a conversion.
        :raises MindeeError: If an invalid path or filename is provided.
        """
        out_path = Path(output_path)
        if not out_path.resolve().is_dir():
            raise MindeeError("Provided path is not a directory.")
        out_file_path = out_path / self.filename
        try:
            self.buffer.seek(0)
            if file_format is None:
                out_file_path.write_bytes(self.buffer.read())
            else:
                image = bernard_image.decode(self.buffer)
                image.save(out_file_path, format=file_format)
            logger.info("File saved successfully to '%s'.", out_file_path)
        except Exception as e:
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
