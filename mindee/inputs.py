import base64
import io
import os
from mimetypes import guess_type
from typing import BinaryIO, Optional, Tuple

import pikepdf

from mindee.logger import logger

ALLOWED_MIME_TYPES = [
    "image/png",
    "image/jpg",
    "image/jpeg",
    "image/webp",
    "application/pdf",
]

INPUT_TYPE_FILE = "file"
INPUT_TYPE_BASE64 = "base64"
INPUT_TYPE_BYTES = "bytes"
INPUT_TYPE_PATH = "path"


class InputDocument:
    file_object: BinaryIO
    filename: str
    file_mimetype: str
    input_type: str
    filepath: Optional[str] = None
    cut_pdf: bool
    n_pdf_pages: int

    def __init__(
        self,
        input_type: str,
        cut_pdf=True,
        n_pdf_pages=3,
    ):
        assert 0 < n_pdf_pages <= 3
        self.input_type = input_type
        self._check_mimetype()

        if self.file_mimetype == "application/pdf":
            self.check_pdf_open()
            count_pages = self.count_pdf_pages()
            if cut_pdf is True:
                if count_pages > 3:
                    self.merge_pdf_pages(
                        [0, count_pages - 2, count_pages - 1][:n_pdf_pages]
                    )
            if self.is_pdf_empty():
                raise AssertionError(f"PDF pages are empty in: {self.filename}")
        logger.debug("Loaded new document '%s' from %s", self.filename, self.input_type)

    def _check_mimetype(self) -> None:
        file_mimetype = guess_type(self.filename)[0]
        if file_mimetype:
            self.file_mimetype = file_mimetype
        else:
            raise AssertionError(f"Could not determine MIME type of '{self.filename}'")

        if self.file_mimetype not in ALLOWED_MIME_TYPES:
            raise AssertionError(
                "File type not allowed, must be one of {%s}"
                % ", ".join(ALLOWED_MIME_TYPES)
            )

    def count_pdf_pages(self) -> int:
        """
        Count the pages in the PDF.

        :return: the number of pages.
        """
        self.file_object.seek(0)
        with pikepdf.open(self.file_object) as pdf:
            return len(pdf.pages)

    def merge_pdf_pages(self, page_numbers: list) -> None:
        """
        Create a new PDF from pages and set it to ``file_object``.

        :param page_numbers: List of pages number to use for merging in the original PDF.
        :return: None
        """
        self.file_object.seek(0)
        new_pdf = pikepdf.Pdf.new()
        with pikepdf.open(self.file_object) as pdf:
            for page_n in page_numbers:
                new_pdf.pages.append(pdf.pages[page_n])
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

    def check_pdf_open(self) -> None:
        """
        Check if the document can be opened using pikepdf.

        :return: None
        """
        self.file_object.seek(0)
        try:
            pikepdf.open(self.file_object)
        except Exception as err:
            raise RuntimeError("Couldn't open PDF file") from err

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


class FileDocument(InputDocument):
    def __init__(
        self,
        file: BinaryIO,
        cut_pdf=True,
        n_pdf_pages=3,
    ):
        """
        Input document from a Python binary file object.

        Note: the calling function is responsible for closing the file.

        :param file: FileIO object
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        """
        assert file.name, "File name must be set"

        self.file_object = file
        self.filename = os.path.basename(file.name)
        self.filepath = file.name

        super().__init__(
            input_type=INPUT_TYPE_FILE,
            cut_pdf=cut_pdf,
            n_pdf_pages=n_pdf_pages,
        )


class PathDocument(InputDocument):
    def __init__(
        self,
        filepath: str,
        cut_pdf=True,
        n_pdf_pages=3,
    ):
        """
        Input document from a path.

        :param filepath: Path to open
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        """
        self.file_object = open(filepath, "rb")  # pylint: disable=consider-using-with
        self.filename = os.path.basename(filepath)
        self.filepath = filepath

        super().__init__(
            input_type=INPUT_TYPE_PATH,
            cut_pdf=cut_pdf,
            n_pdf_pages=n_pdf_pages,
        )


class BytesDocument(InputDocument):
    def __init__(
        self,
        raw_bytes: bytes,
        filename: str,
        cut_pdf=True,
        n_pdf_pages=3,
    ):
        """
        Input document from raw bytes (no buffer).

        :param raw_bytes: Raw data as bytes
        :param filename: File name of the input
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        """
        self.file_object = io.BytesIO(raw_bytes)

        self.filename = filename
        self.filepath = None

        super().__init__(
            input_type=INPUT_TYPE_BYTES,
            cut_pdf=cut_pdf,
            n_pdf_pages=n_pdf_pages,
        )


class Base64Document(InputDocument):
    def __init__(
        self,
        base64_string: str,
        filename: str,
        cut_pdf=True,
        n_pdf_pages=3,
    ):
        """
        Input document from a base64 encoded string.

        :param base64_string: Raw data as a base64 encoded string
        :param filename: File name of the input
        :param cut_pdf: Automatically reconstruct pdf with more than N pages
        """
        self.file_object = io.BytesIO(base64.standard_b64decode(base64_string))
        self.filename = filename
        self.filepath = None

        super().__init__(
            input_type=INPUT_TYPE_BASE64,
            cut_pdf=cut_pdf,
            n_pdf_pages=n_pdf_pages,
        )
