from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

from mindee.dependencies.checkers import BERNARD_LEDIT_AVAILABLE
from mindee.error.mindee_error import MindeeError
from mindee.input.bytes_input import BytesInput

if BERNARD_LEDIT_AVAILABLE:
    # pylint: disable=import-error
    import bernard_ledit.common as bernard_common
else:
    bernard_common = None  # type: ignore[assignment]  # pylint: disable=invalid-name


class ExtractedPDF:
    """An extracted sub-Pdf."""

    buffer: BinaryIO
    """PDF content as a byte stream."""
    filename: str
    """Name of the file when writing to disk."""
    _page_indexes: list[int]

    def __init__(
        self, pdf_byte_stream: BinaryIO, filename: str, page_indexes: list[int]
    ):
        self.buffer = pdf_byte_stream
        self.filename = filename
        self._page_indexes = page_indexes

    def write_to_file(self, output_path: Path | str):
        """
        Writes the contents of the current PDF object to a file.

        :param output_path: Path of the destination file.
        If the extension doesn't identify a PDF, '.pdf' is appended.
        """
        out_path = Path(output_path)
        if not out_path.resolve().is_dir():
            raise MindeeError("Provided path is not a directory.")
        out_file_path = out_path / self.filename
        is_pdf = (
            bernard_common.format_from_extension(out_file_path.suffix) == "PDF"
            if bernard_common is not None
            else out_file_path.suffix.lower() == ".pdf"
        )
        if not is_pdf:
            out_file_path = out_file_path.with_name(f"{out_file_path.name}.pdf")

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
    def page_indexes(self) -> list[int]:
        """
        0-based indexes of all pages taken from the original PDF.
        """
        return self._page_indexes

    @property
    def page_count(self) -> int:
        """The number of pages in this PDF file."""
        return len(self._page_indexes)
