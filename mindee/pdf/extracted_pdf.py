from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

from mindee.error.mindee_error import MindeeError
from mindee.input.bytes_input import BytesInput


class ExtractedPDF:
    """An extracted sub-Pdf."""

    buffer: BinaryIO
    """PDF content as a byte stream."""
    filename: str
    """Name of the file when writing to disk."""
    _page_range: tuple[int, int]

    def __init__(
        self, pdf_byte_stream: BinaryIO, filename: str, page_range: tuple[int, int]
    ):
        self.buffer = pdf_byte_stream
        self.filename = filename
        self._page_range = page_range

    def write_to_file(self, output_path: Path | str):
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
    def page_range(self) -> tuple[int, int]:
        """
        This PDF was extracted from this page range of the original PDF.
        The first number is the index of the first page.
        The second number is the index of the last page.
        """
        return self._page_range

    @property
    def page_count(self) -> int:
        """The number of pages in this PDF file."""
        return self._page_range[1] - self._page_range[0] + 1
