import base64
import io
import mimetypes
import os
from enum import Enum
from typing import BinaryIO, Optional, Sequence, Tuple

import pikepdf

from mindee.input.page_options import KEEP_ONLY, REMOVE
from mindee.logger import logger

mimetypes.add_type("image/heic", ".heic")
mimetypes.add_type("image/heic", ".heif")

ALLOWED_MIME_TYPES = [
    "application/pdf",
    "image/heic",
    "image/png",
    "image/jpg",
    "image/jpeg",
    "image/tiff",
    "image/webp",
]


class InputType(Enum):
    """The input type, for internal use."""

    FILE = "file"
    BASE64 = "base64"
    BYTES = "bytes"
    PATH = "path"
    URL = "url"


class MimeTypeError(AssertionError):
    """The MIME Type is not valid."""


class LocalInputSource:
    """Base class for all input sources coming from the local machine."""

    file_object: BinaryIO
    filename: str
    file_mimetype: str
    input_type: InputType
    filepath: Optional[str] = None

    def __init__(
        self,
        input_type: InputType,
    ):
        self.input_type = input_type
        self._check_mimetype()

        logger.debug("Loaded new input '%s' from %s", self.filename, self.input_type)

    def _check_mimetype(self) -> None:
        file_mimetype = mimetypes.guess_type(self.filename)[0]
        if file_mimetype:
            self.file_mimetype = file_mimetype
        else:
            raise MimeTypeError(f"Could not determine MIME type of '{self.filename}'")

        if self.file_mimetype not in ALLOWED_MIME_TYPES:
            file_types = ", ".join(ALLOWED_MIME_TYPES)
            raise MimeTypeError(f"File type not allowed, must be one of {file_types}")

    def is_pdf(self) -> bool:
        """:return: True if the file is a PDF."""
        return self.file_mimetype == "application/pdf"

    def count_doc_pages(self) -> int:
        """
        Count the pages in the PDF.

        :return: the number of pages.
        """
        self.file_object.seek(0)
        with pikepdf.open(self.file_object) as pdf:
            return len(pdf.pages)

    def process_pdf(
        self,
        behavior: str,
        on_min_pages: int,
        page_indexes: Sequence,
    ) -> None:
        """Run any required processing on a PDF file."""
        if self.is_pdf_empty():
            raise AssertionError(f"PDF pages are empty in: {self.filename}")
        pages_count = self.count_doc_pages()
        if on_min_pages > pages_count:
            return
        all_pages = list(range(pages_count))
        if behavior == KEEP_ONLY:
            pages_to_keep = set()
            for page_id in page_indexes:
                try:
                    pages_to_keep.add(all_pages[page_id])
                except IndexError:
                    logger.warning("Page index not in source document: %s", page_id)
        elif behavior == REMOVE:
            pages_to_remove = set()
            for page_id in page_indexes:
                try:
                    pages_to_remove.add(all_pages[page_id])
                except IndexError:
                    logger.warning("Page index not in source document: %s", page_id)
            pages_to_keep = pages_to_remove.symmetric_difference(set(all_pages))
        else:
            raise AssertionError(f"Invalid cut behavior specified: {behavior}")

        if len(pages_to_keep) < 1:
            raise RuntimeError("Resulting PDF would have no pages left.")
        self.merge_pdf_pages(pages_to_keep)

    def merge_pdf_pages(self, page_numbers: set) -> None:
        """
        Create a new PDF from pages and set it to ``file_object``.

        :param page_numbers: List of pages number to use for merging in the original PDF.
        :return: None
        """
        self.file_object.seek(0)
        new_pdf = pikepdf.Pdf.new()
        with pikepdf.open(self.file_object) as pdf:
            for page_id in page_numbers:
                page = pdf.pages[page_id]
                new_pdf.pages.append(page)
        self.file_object.close()
        self.file_object = io.BytesIO()
        new_pdf.save(self.file_object)

    def is_pdf_empty(self) -> bool:
        """
        Check if the PDF is empty.

        :return: ``True`` if the PDF is empty
        """
        self.file_object.seek(0)
        with pikepdf.open(self.file_object) as pdf:
            for page in pdf.pages:
                # mypy incorrectly identifies the "/Length" key's value as
                # an object rather than an int.
                try:
                    total_size = page["/Contents"]["/Length"]
                except ValueError:
                    total_size = 0  # type: ignore
                    for content in page["/Contents"]:  # type: ignore
                        total_size += content["/Length"]
                has_data = total_size > 1000  # type: ignore

                has_font = "/Font" in page["/Resources"].keys()
                has_xobj = "/XObject" in page["/Resources"].keys()

                if has_font or has_xobj or has_data:
                    return False
            return True

    def read_contents(self, close_file: bool) -> Tuple[str, bytes]:
        """
        Read the contents of the input file.

        :param close_file: whether to close the file after reading
        :return: a Tuple with the file name and binary data
        """
        logger.debug("Reading data from: %s", self.filename)
        self.file_object.seek(0)
        data = self.file_object.read()
        if close_file:
            self.file_object.close()
        else:
            self.file_object.seek(0)
        return self.filename, data

    def close(self) -> None:
        """Close the file object."""
        self.file_object.close()



class FileInput(LocalInputSource):
    """A binary file input."""

    def __init__(self, file: BinaryIO) -> None:
        """
        Input document from a Python binary file object.

        Note: the calling function is responsible for closing the file.

        :param file: FileIO object
        """
        assert file.name, "File name must be set"

        self.file_object = file
        self.filename = os.path.basename(file.name)
        self.filepath = file.name
        super().__init__(input_type=InputType.FILE)


class PathInput(LocalInputSource):
    """A local path input."""

    def __init__(self, filepath: str) -> None:
        """
        Input document from a path.

        :param filepath: Path to open
        """
        self.file_object = open(filepath, "rb")  # pylint: disable=consider-using-with
        self.filename = os.path.basename(filepath)
        self.filepath = filepath
        super().__init__(input_type=InputType.PATH)


class BytesInput(LocalInputSource):
    """Raw bytes input."""

    def __init__(self, raw_bytes: bytes, filename: str) -> None:
        """
        Input document from raw bytes (no buffer).

        :param raw_bytes: Raw data as bytes
        :param filename: File name of the input
        """
        self.file_object = io.BytesIO(raw_bytes)
        self.filename = filename
        self.filepath = None
        super().__init__(input_type=InputType.BYTES)


class Base64Input(LocalInputSource):
    """Base64-encoded text input."""

    def __init__(self, base64_string: str, filename: str) -> None:
        """
        Input document from a base64 encoded string.

        :param base64_string: Raw data as a base64 encoded string
        :param filename: File name of the input
        """
        self.file_object = io.BytesIO(base64.standard_b64decode(base64_string))
        self.filename = filename
        self.filepath = None
        super().__init__(input_type=InputType.BASE64)


class UrlInputSource:
    """A local or distant URL input."""

    url: str
    """The Uniform Resource Locator."""

    def __init__(self, url: str) -> None:
        """
        Input document from a base64 encoded string.

        :param url: URL to send, must be HTTPS
        """
        if not url.lower().startswith("https"):
            raise AssertionError("URL must be HTTPS")

        self.input_type = InputType.URL

        logger.debug("URL input: %s", url)

        self.url = url
