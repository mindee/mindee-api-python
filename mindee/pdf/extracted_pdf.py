from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

from mindee.dependencies.checkers import PYPDFIUM2_AVAILABLE
from mindee.dependencies.decorators import requires_pypdfium2
from mindee.error.mindee_error import MindeeError
from mindee.input.bytes_input import BytesInput

if PYPDFIUM2_AVAILABLE:
    # pylint: disable=import-error
    import pypdfium2 as pdfium
else:
    pdfium = None  # pylint: disable=invalid-name


class ExtractedPDF:
    """An extracted sub-Pdf."""

    buffer: BinaryIO
    filename: str
    _page_indexes: tuple[int, int]

    def __init__(
        self, pdf_byte_stream: BinaryIO, filename: str, page_indexes: tuple[int, int]
    ):
        self.buffer = pdf_byte_stream
        self.filename = filename
        self._page_indexes = page_indexes

    @requires_pypdfium2
    def get_page_count(self) -> int:
        """Get the number of pages in the PDF file."""
        try:
            pdf = pdfium.PdfDocument(self.buffer)
            return len(pdf)
        except Exception as e:
            raise MindeeError(
                "Could not retrieve page count from Extracted PDF object."
            ) from e

    def save_to_file(self, output_path: Path | str):
        """
        Writes the contents of the current PDF object to a file.

        :param output_path: Path of the destination file.
        If no extension is provided, '.pdf' will be appended by default.
        """
        out_path = Path(output_path)
        if not out_path.resolve().is_dir():
            raise MindeeError("Provided path is not a directory.")
        out_file_path = out_path / self.filename

        try:
            self.buffer.seek(0)
            with open(out_file_path, "wb") as out_file:
                out_file.write(self.buffer.read())
        except Exception as e:
            print(e)
            raise MindeeError(f"Could not save file {out_file_path}.") from e

    def as_input_source(self) -> BytesInput:
        """Returns the current PDF object as a usable BytesInput source."""
        self.buffer.seek(0)
        return BytesInput(self.buffer.read(), self.filename)

    @property
    def page_indexes(self) -> tuple[int, int]:
        """This PDF was extracted from this page range of the original PDF."""
        return self._page_indexes
