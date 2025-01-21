import io
from pathlib import Path
from typing import Optional

from PIL import Image

from mindee.error.mindee_error import MindeeError
from mindee.input.sources.file_input import FileInput
from mindee.input.sources.local_input_source import LocalInputSource
from mindee.logger import logger


class ExtractedImage:
    """Generic class for image extraction."""

    _page_id: int
    """Id of the page the image was extracted from."""
    _element_id: int
    """Id of the element on a given page."""

    def __init__(
        self, input_source: LocalInputSource, page_id: int, element_id: int
    ) -> None:
        """
        Initialize the ExtractedImage with a buffer and an internal file name.

        :param input_source: Local source for input.
        :param page_id: ID of the page the element was found on.
        :param element_id: ID of the element in a page.
        """
        self.buffer = io.BytesIO(input_source.file_object.read())
        self.buffer.name = input_source.filename
        if input_source.is_pdf():
            extension = "jpg"
        else:
            extension = Path(input_source.filename).resolve().suffix
        self.buffer.seek(0)
        pg_number = str(page_id).zfill(3)
        elem_number = str(element_id).zfill(3)
        self.internal_file_name = (
            f"{input_source.filename}_page{pg_number}-{elem_number}.{extension}"
        )
        self._page_id = page_id
        self._element_id = 0 if element_id is None else element_id

    def save_to_file(self, output_path: str, file_format: Optional[str] = None):
        """
        Saves the document to a file.

        :param output_path: Path to save the file to.
        :param file_format: Optional PIL-compatible format for the file. Inferred from file extension if not provided.
        :raises MindeeError: If an invalid path or filename is provided.
        """
        try:
            resolved_path = Path(output_path).resolve()
            if not file_format:
                if len(resolved_path.suffix) < 1:
                    raise ValueError("Invalid file format.")
                file_format = (
                    resolved_path.suffix.upper()
                )  # technically redundant since PIL applies an upper operation
                # to the parameter , but older versions may not do so.
            self.buffer.seek(0)
            image = Image.open(self.buffer)
            image.save(resolved_path, format=file_format)
            logger.info("File saved successfully to '%s'.", resolved_path)
        except TypeError as exc:
            raise MindeeError("Invalid path/filename provided.") from exc
        except Exception as exc:
            raise MindeeError(f"Could not save file {Path(output_path).name}.") from exc

    def as_source(self) -> FileInput:
        """
        Return the file as a Mindee-compatible BufferInput source.

        :returns: A BufferInput source.
        """
        self.buffer.seek(0)
        return FileInput(self.buffer)

    @property
    def page_id(self):
        """
        ID of the page the receipt was found on.

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
