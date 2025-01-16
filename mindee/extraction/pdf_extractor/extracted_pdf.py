from pathlib import Path
from typing import BinaryIO

import pypdfium2 as pdfium

from mindee.error.mindee_error import MindeeError
from mindee.input.sources.bytes_input import BytesInput


class ExtractedPdf:
    """An extracted sub-Pdf."""

    pdf_bytes: BinaryIO
    filename: str

    def __init__(self, pdf_bytes: BinaryIO, filename: str):
        self.pdf_bytes = pdf_bytes
        self.filename = filename

    def get_page_count(self) -> int:
        """Get the number of pages in the PDF file."""
        try:
            pdf = pdfium.PdfDocument(self.pdf_bytes)
            return len(pdf)
        except Exception as exc:
            raise MindeeError(
                "Could not retrieve page count from Extracted PDF object."
            ) from exc

    def write_to_file(self, output_path: str):
        """
        Writes the contents of the current PDF object to a file.

        :param output_path: Path of the destination file. If not extension is provided, pdf will be appended by default.
        """
        out_path = Path(output_path)
        if out_path.resolve().is_dir():
            raise MindeeError("Provided path is not a file.")
        if not output_path or not out_path.parent.exists():
            raise MindeeError("Invalid save path provided {}.")
        if out_path.suffix.lower() != "pdf":
            out_path = out_path.parent / (out_path.stem + "." + "pdf")
        with open(out_path, "wb") as out_file:
            out_file.write(self.pdf_bytes.read())

    def as_input_source(self) -> BytesInput:
        """Returns the current PDF object as a usable BytesInput source."""
        self.pdf_bytes.seek(0)
        return BytesInput(self.pdf_bytes.read(), self.filename)
