import base64
import io
import mimetypes
import os
import tempfile
from enum import Enum
from pathlib import Path
from typing import BinaryIO, Optional, Sequence, Tuple, Union

import pypdfium2 as pdfium

from mindee.error.mimetype_error import MimeTypeError
from mindee.error.mindee_error import MindeeError, MindeeSourceError
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


class LocalInputSource:
    """Base class for all input sources coming from the local machine."""

    file_object: BinaryIO
    filename: str
    file_mimetype: str
    input_type: InputType
    filepath: Optional[str]

    def __init__(self, input_type: InputType):
        self.input_type = input_type
        self._check_mimetype()

        logger.debug("Loaded new input '%s' from %s", self.filename, self.input_type)

    def _check_mimetype(self) -> None:
        file_mimetype = mimetypes.guess_type(self.filename)[0]
        if file_mimetype:
            self.file_mimetype = file_mimetype
        else:
            raise MimeTypeError(f"Could not determine MIME type of '{self.filename}'.")

        if self.file_mimetype not in ALLOWED_MIME_TYPES:
            file_types = ", ".join(ALLOWED_MIME_TYPES)
            raise MimeTypeError(f"File type not allowed, must be one of {file_types}.")

    def fix_pdf(self, maximum_offset: int = 500) -> None:
        """
        Fix a potentially broken pdf file.

        WARNING: this feature alters the data of the enqueued file by removing unnecessary headers.

        Reads the bytes of a PDF file until a proper pdf tag is encountered,
        or until the maximum offset has been reached.
        If a tag denoting a PDF file is found, deletes all bytes before it.

        :param maximum_offset: maximum byte offset where superfluous headers will be removed.
            Cannot be less than 0.
        """
        if maximum_offset < 0:
            raise MindeeError("Can't set maximum offset for pdf-fixing to less than 0.")
        try:
            buf = self.file_object.read()
            self.file_object.seek(0)
            pos: int = buf.find(b"%PDF-")
            if pos != -1 and pos < maximum_offset:
                self.file_object.seek(pos)
                raw_bytes = self.file_object.read()
                temp_file = tempfile.TemporaryFile()
                temp_file.write(raw_bytes)
                temp_file.seek(0)
                self.file_object = io.BytesIO(temp_file.read())
                temp_file.close()
            else:
                if pos < 0:
                    raise MimeTypeError(
                        "Provided stream isn't a valid PDF-like object."
                    )
                raise MimeTypeError(
                    f"PDF couldn't be fixed. PDF tag was found at position {pos}."
                )
            self.file_mimetype = "application/pdf"
        except MimeTypeError as exc:
            raise exc
        except Exception as exc:
            print(f"Attempt to fix pdf raised exception {exc}.")
            raise exc

    def is_pdf(self) -> bool:
        """:return: True if the file is a PDF."""
        return self.file_mimetype == "application/pdf"

    def count_doc_pages(self) -> int:
        """
        Count the pages in the PDF.

        :return: the number of pages.
        """
        if self.is_pdf():
            self.file_object.seek(0)
            pdf = pdfium.PdfDocument(self.file_object)
            return len(pdf)
        return 1

    def process_pdf(
        self,
        behavior: str,
        on_min_pages: int,
        page_indexes: Sequence,
    ) -> None:
        """Run any required processing on a PDF file."""
        if self.is_pdf_empty():
            raise MindeeSourceError(f"PDF pages are empty in: {self.filename}")
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
            raise MindeeSourceError(f"Invalid cut behavior specified: {behavior}")

        if len(pages_to_keep) < 1:
            raise MindeeSourceError("Resulting PDF would have no pages left.")
        self.merge_pdf_pages(pages_to_keep)

    def merge_pdf_pages(self, page_numbers: set) -> None:
        """
        Create a new PDF from pages and set it to ``file_object``.

        :param page_numbers: List of pages number to use for merging in the original PDF.
        :return: None
        """
        self.file_object.seek(0)
        new_pdf = pdfium.PdfDocument.new()
        pdf = pdfium.PdfDocument(self.file_object)
        new_pdf.import_pages(pdf, list(page_numbers))
        self.file_object.close()
        bytes_io = io.BytesIO()
        new_pdf.save(bytes_io)
        self.file_object = bytes_io

    def is_pdf_empty(self) -> bool:
        """
        Check if the PDF is empty.

        :return: ``True`` if the PDF is empty
        """
        self.file_object.seek(0)
        pdf = pdfium.PdfDocument(self.file_object)
        for page in pdf:
            for _ in page.get_objects():
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

    def __init__(self, filepath: Union[Path, str]) -> None:
        """
        Input document from a path.

        :param filepath: Path to open
        """
        self.file_object = open(filepath, "rb")  # pylint: disable=consider-using-with
        self.filename = os.path.basename(filepath)
        self.filepath = str(filepath)
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
            raise MindeeSourceError("URL must be HTTPS")

        self.input_type = InputType.URL

        logger.debug("URL input: %s", url)

        self.url = url
