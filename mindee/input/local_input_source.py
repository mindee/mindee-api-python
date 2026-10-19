from __future__ import annotations

import io
import mimetypes
from typing import BinaryIO

from mindee.dependencies import requires_bernard_ledit
from mindee.dependencies.checkers import BERNARD_LEDIT_AVAILABLE
from mindee.error.mimetype_error import MimeTypeError
from mindee.error.mindee_error import MindeeError, MindeeSourceError
from mindee.input.page_options import PageOptions
from mindee.logger import logger
from mindee.pdf.pdf_utils import pdf_has_source_text

if BERNARD_LEDIT_AVAILABLE:
    # pylint: disable=import-error
    import bernard_ledit.image as bernard_image
    import bernard_ledit.pdf as bernard_pdf
else:
    bernard_pdf = None  # type: ignore[assignment]  # pylint: disable=invalid-name
    bernard_image = None  # type: ignore[assignment]  # pylint: disable=invalid-name

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
            # Some broken (yet fixable) PDFs can cause Bernard to crash on open.
            if BERNARD_LEDIT_AVAILABLE:
                try:
                    pdf = bernard_pdf.PdfDocument(self.file_object)
                    self.page_count = len(pdf)
                except bernard_pdf.PdfiumError as e:
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

    def is_pdf(self) -> bool:
        """:return: True if the file is a PDF."""
        return self.file_mimetype == "application/pdf"

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
        self.file_object.seek(0)
        try:
            fixed = bernard_pdf.fix_pdf(self.file_object, maximum_offset)
        except bernard_pdf.PdfFixError as e:
            raise MimeTypeError(str(e)) from e
        self.file_object = io.BytesIO(fixed)
        self.file_mimetype = "application/pdf"

    @requires_bernard_ledit
    def apply_page_options(self, page_options: PageOptions) -> None:
        """Apply cut and merge options on multipage documents."""
        if not self.is_pdf():
            raise MindeeSourceError(f"File is not a PDF: {self.filename}")
        self.file_object.seek(0)
        try:
            doc, skipped = bernard_pdf.apply_page_options(
                self.file_object,
                page_options.operation,
                page_options.on_min_pages,
                list(page_options.page_indexes),
            )
            page_count = len(doc or [])
        except bernard_pdf.PageOptionsError as e:
            raise MindeeSourceError(f"{e} ({self.filename})") from e
        for page_id in skipped:
            logger.warning("Page index not in source document: %s", page_id)
        if doc is None:
            return
        self.file_object.close()
        with doc:
            self.file_object = io.BytesIO(doc.as_bytes())
        self.page_count = page_count

    @requires_bernard_ledit
    def is_pdf_empty(self) -> bool:
        """
        Check if the PDF is empty.

        :return: ``True`` if the PDF is empty
        """
        self.file_object.seek(0)
        with bernard_pdf.PdfDocument(self.file_object) as pdf:
            return pdf.has_no_content()
        raise MindeeSourceError("Failed to read PDF")

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

    @requires_bernard_ledit
    def compress(
        self,
        quality: int = 85,
        max_width: int | None = None,
        max_height: int | None = None,
    ) -> None:
        """
        Compresses the file object, either as a PDF or an image.

        :param quality: Quality of the compression. For images, this is the JPEG quality.
            For PDFs, this affects image quality within the PDF.
        :param max_width: Maximum width for image resizing. Ignored for PDFs.
        :param max_height: Maximum height for image resizing. Ignored for PDFs.
        """

        self.file_object.seek(0)
        data = self.file_object.read()
        if self.is_pdf():
            compressed = bernard_pdf.compress(data, quality)
        else:
            compressed = bernard_image.compress(data, quality, max_width, max_height)

        self.file_object = io.BytesIO(compressed)
        self.file_object.seek(0)

    def __enter__(self):
        """Allows the class to be used as a context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensures the file is closed when the context block exits."""
        if self.file_object and not self.file_object.closed:
            self.file_object.close()
