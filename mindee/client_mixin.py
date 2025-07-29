from pathlib import Path
from typing import BinaryIO, Union

from mindee.error import MindeeClientError
from mindee.input import Base64Input, BytesInput, FileInput, PathInput, UrlInputSource


class ClientMixin:
    """Mixin for clients V1 & V2 common static methods."""

    @staticmethod
    def source_from_path(
        input_path: Union[Path, str], fix_pdf: bool = False
    ) -> PathInput:
        """
        Load a document from a path, as a string or a `Path` object.

        :param input_path: Path of file to open
        :param fix_pdf: Whether to attempt fixing PDF files before sending.
            Setting this to `True` can modify the data sent to Mindee.
        """
        input_doc = PathInput(input_path)
        if fix_pdf:
            input_doc.fix_pdf()
        return input_doc

    @staticmethod
    def source_from_file(input_file: BinaryIO, fix_pdf: bool = False) -> FileInput:
        """
        Load a document from a normal Python file object/handle.

        :param input_file: Input file handle
        :param fix_pdf: Whether to attempt fixing PDF files before sending.
            Setting this to `True` can modify the data sent to Mindee.
        """
        input_doc = FileInput(input_file)
        if fix_pdf:
            input_doc.fix_pdf()
        return input_doc

    @staticmethod
    def source_from_b64string(
        input_string: str, filename: str, fix_pdf: bool = False
    ) -> Base64Input:
        """
        Load a document from a base64 encoded string.

        :param input_string: Input to parse as base64 string
        :param filename: The name of the file (without the path)
        :param fix_pdf: Whether to attempt fixing PDF files before sending.
            Setting this to `True` can modify the data sent to Mindee.
        """
        input_doc = Base64Input(input_string, filename)
        if fix_pdf:
            input_doc.fix_pdf()
        return input_doc

    @staticmethod
    def source_from_bytes(
        input_bytes: bytes, filename: str, fix_pdf: bool = False
    ) -> BytesInput:
        """
        Load a document from raw bytes.

        :param input_bytes: Raw byte input
        :param filename: The name of the file (without the path)
        :param fix_pdf: Whether to attempt fixing PDF files before sending.
            Setting this to `True` can modify the data sent to Mindee.
        """
        input_doc = BytesInput(input_bytes, filename)
        if fix_pdf:
            input_doc.fix_pdf()
        return input_doc

    @staticmethod
    def _validate_async_params(
        initial_delay_sec: float, delay_sec: float, max_retries: int
    ) -> None:
        min_delay = 1
        min_initial_delay = 1
        min_retries = 1
        if delay_sec < min_delay:
            raise MindeeClientError(
                f"Cannot set auto-parsing delay to less than {min_delay} second(s)."
            )
        if initial_delay_sec < min_initial_delay:
            raise MindeeClientError(
                f"Cannot set initial parsing delay to less than {min_initial_delay} second(s)."
            )
        if max_retries < min_retries:
            raise MindeeClientError(f"Cannot set retries to less than {min_retries}.")

    @staticmethod
    def source_from_url(
        url: str,
    ) -> UrlInputSource:
        """
        Load a document from a URL.

        :param url: Raw byte input
        """
        return UrlInputSource(
            url,
        )
