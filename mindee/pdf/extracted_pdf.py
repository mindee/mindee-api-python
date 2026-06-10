from pathlib import Path
from typing import BinaryIO

from mindee.dependencies.checkers import PYPDFIUM2_AVAILABLE
from mindee.dependencies.decorators import requires_pypdfium2
from mindee.error.mindee_error import MindeeError
from mindee.input.bytes_input import BytesInput

if PYPDFIUM2_AVAILABLE:
    import pypdfium2 as pdfium
else:
    pdfium = None  # pylint: disable=invalid-name


class ExtractedPDF:
    """An extracted sub-Pdf."""

    pdf_bytes: BinaryIO
    filename: str

    def __init__(self, pdf_bytes: BinaryIO, filename: str):
        self.pdf_bytes = pdf_bytes
        self.filename = filename

    @requires_pypdfium2
    def get_page_count(self) -> int:
        """Get the number of pages in the PDF file."""
        try:
            pdf = pdfium.PdfDocument(self.pdf_bytes)
            return len(pdf)
        except Exception as e:
            raise MindeeError(
                "Could not retrieve page count from Extracted PDF object."
            ) from e

    def save_to_file(self, output_path: Path | str):
        """
        Writes the contents of the current PDF object to a file.

        :param output_path: Path of the destination file. If
         not extension is provided, pdf will be appended by default.
        """
        out_path = Path(output_path)
        if out_path.resolve().is_dir():
            raise MindeeError("Provided path is not a file.")
        if not output_path or not out_path.parent.exists():
            raise MindeeError("Invalid save path provided {}.")
        if out_path.suffix.lower() != "pdf":
            out_path = out_path.parent / (out_path.stem + "." + "pdf")
        self.pdf_bytes.seek(0)
        with open(out_path, "wb") as out_file:
            out_file.write(self.pdf_bytes.read())

    def as_input_source(self) -> BytesInput:
        """Returns the current PDF object as a usable BytesInput source."""
        self.pdf_bytes.seek(0)
        return BytesInput(self.pdf_bytes.read(), self.filename)
