import io
from pathlib import Path

from mindee.error import MindeeError
from mindee.input import FileInput
from mindee.logger import logger


class ExtractedImage:
    def __init__(self, buffer: bytes, file_name: str):
        """
        Initialize the ExtractedImage with a buffer and an internal file name.

        :param buffer: The byte buffer representing the image.
        :param file_name: The internal file name of the image.
        """
        self.buffer = io.BytesIO(buffer)
        self.internal_file_name = file_name

    def save_to_file(self, output_path: str):
        """
        Saves the document to a file.

        :param output_path: Path to save the file to.
        :raises MindeeError: If an invalid path or filename is provided.
        """
        try:
            resolved_path = Path(output_path).resolve()
            with open(resolved_path, 'wb') as f:
                f.write(self.buffer.read())
            logger.info(f"File saved successfully to {resolved_path}.")
        except TypeError:
            raise MindeeError("Invalid path/filename provided.")
        except Exception as e:
            raise e

    def as_source(self) -> FileInput:
        """
        Return the file as a Mindee-compatible BufferInput source.

        :returns: A BufferInput source.
        """
        return FileInput(self.buffer)
