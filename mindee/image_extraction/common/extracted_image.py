import io
from pathlib import Path
from typing import Optional

from PIL import Image

from mindee.error import MindeeError
from mindee.input import FileInput
from mindee.logger import logger


class ExtractedImage:
    """Generic class for image extraction."""

    page_id: int
    """Id of the page the image was extracted from."""

    def __init__(self, buffer: bytes, file_name: str):
        """
        Initialize the ExtractedImage with a buffer and an internal file name.

        :param buffer: The byte buffer representing the image.
        :param file_name: The internal file name of the image.
        """
        self.buffer = io.BytesIO(buffer)
        self.internal_file_name = file_name
        self.buffer.name = self.internal_file_name

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
        return FileInput(self.buffer)
