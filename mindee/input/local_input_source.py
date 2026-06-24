from __future__ import annotations

import io
import mimetypes
import tempfile
from collections.abc import Sequence
from typing import BinaryIO

from mindee.dependencies import requires_pypdfium2
from mindee.dependencies.checkers import PYPDFIUM2_AVAILABLE
from mindee.error.mimetype_error import MimeTypeError
from mindee.error.mindee_error import MindeeError, MindeeSourceError
from mindee.image.image_compressor import compress_image
from mindee.input.page_options import KEEP_ONLY, REMOVE, PageOptions
from mindee.logger import logger
from mindee.pdf.pdf_compressor import compress_pdf
from mindee.pdf.pdf_utils import pdf_has_source_text

if PYPDFIUM2_AVAILABLE:
    # pylint: disable=import-error
    import pypdfium2 as pdfium
else:
    pdfium = None  # pylint: disable=invalid-name

mimetypes.add_type("image/heic", ".heic")
mimetypes.add_type("image/heif", ".heif")

ALLOWED_MIME_TYPES = [
    "application/pdf",
    "image/heic",
    "image/heif",
    "image/png",
    "image/jpg",
    "image/jpeg",
    "image/tiff",
    "image/webp",
]


class LocalInputSource:
    """Base class for all input sources coming from the local machine."""

    file_object: BinaryIO
    filename: str
    file_mimetype: str
    filepath: str | None
    page_count: int

    def __init__(self) -> None:
        """
        Initialize a LocalInputSource object.
        """
        self._check_mimetype()
        if self.is_pdf():
            self.file_object.seek(0)
            # Some broken (yet fixable) PDFs can cause pdfium to crash on open.
            if PYPDFIUM2_AVAILABLE:
                try:
                    pdf = pdfium.PdfDocument(self.file_object)
                    self.page_count = len(pdf)
                except pdfium.PdfiumError as e:
                    logger.warning(
                        "Could not open PDF file: %s due to %s", self.filename, e
                    )
                    self.page_count = 0
                self.file_object.seek(0)
            else:
                self.page_count = 0
        else:
            self.page_count = 1
        logger.debug(
            "Loaded new input '%s' from %s", self.filename, {type(self).__name__}
        )

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
                with tempfile.TemporaryFile() as temp_file:
                    temp_file.write(raw_bytes)
                    temp_file.seek(0)
                    self.file_object = io.BytesIO(temp_file.read())
            else:
                if pos < 0:
                    raise MimeTypeError(
                        "Provided stream isn't a valid PDF-like object."
                    )
                raise MimeTypeError(
                    f"PDF couldn't be fixed. PDF tag was found at position {pos}."
                )
            self.file_mimetype = "application/pdf"
        except MimeTypeError as e:
            raise e
        except Exception as e:
            logger.error("Attempt to fix pdf raised exception %s.", e)
            raise e

    def is_pdf(self) -> bool:
        """:return: True if the file is a PDF."""
        return self.file_mimetype == "application/pdf"

    @requires_pypdfium2
    def apply_page_options(self, page_options: PageOptions) -> None:
        """Apply cut and merge options on multipage documents."""
        if not self.is_pdf():
            raise MindeeSourceError(f"File is not a PDF: {self.filename}")
        self.process_pdf(
            page_options.operation,
            page_options.on_min_pages,
            page_options.page_indexes,
        )
        self.file_object.seek(0)
        pdf = pdfium.PdfDocument(self.file_object)
        self.page_count = len(pdf)
        pdf.close()

    def process_pdf(
        self,
        behavior: str,
        on_min_pages: int,
        page_indexes: Sequence[int],
    ) -> None:
        """Run any required processing on a PDF file."""
        if self.is_pdf_empty():
            raise MindeeSourceError(f"PDF pages are empty in: {self.filename}")
        page_count = self.page_count
        if on_min_pages > page_count:
            return
        all_pages = list(range(page_count))
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

    @requires_pypdfium2
    def merge_pdf_pages(self, page_numbers: set) -> None:
        """
        Create a new PDF from pages and set it to ``file_object``.

        :param page_numbers: List of page numbers to use for merging in the original PDF.
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
        self.page_count = len(new_pdf)
        new_pdf.close()
        pdf.close()

    @requires_pypdfium2
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

    def read_contents(self, close_file: bool) -> tuple[str, bytes]:
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

    def close(self):
        """Allow explicit closing for users not using a context manager."""
        if self.file_object and not self.file_object.closed:
            self.file_object.close()

    def has_source_text(self) -> bool:
        """
        If the file is a PDF, checks if it has source text.

        :return: True if the file is a PDF and has source text. False otherwise.
        """
        if not self.is_pdf():
            return False
        return pdf_has_source_text(self.file_object.read())

    @requires_pypdfium2
    def compress(
        self,
        quality: int = 85,
        max_width: int | None = None,
        max_height: int | None = None,
        force_source_text: bool = False,
        disable_source_text: bool = True,
    ) -> None:
        """
        Compresses the file object, either as a PDF or an image.

        :param quality: Quality of the compression. For images, this is the JPEG quality.
            For PDFs, this affects image quality within the PDF.
        :param max_width: Maximum width for image resizing. Ignored for PDFs.
        :param max_height: Maximum height for image resizing. Ignored for PDFs.
        :param force_source_text: For PDFs, whether to force compression even if source text is present.
        :param disable_source_text: For PDFs, whether to disable source text during compression.
        """
        new_file_bytes: bytes
        if self.is_pdf():
            new_file_bytes = compress_pdf(
                self.file_object, quality, force_source_text, disable_source_text
            )
        else:
            new_file_bytes = compress_image(
                self.file_object, quality, max_width, max_height
            )

        self.file_object = io.BytesIO(new_file_bytes)

    def __enter__(self):
        """Allows the class to be used as a context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensures the file is closed when the context block exits."""
        if self.file_object and not self.file_object.closed:
            self.file_object.close()
