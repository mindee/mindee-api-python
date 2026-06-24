from __future__ import annotations

import io
from pathlib import Path
from typing import Any, BinaryIO

from mindee.dependencies.checkers import PILLOW_AVAILABLE, PYPDFIUM2_AVAILABLE
from mindee.dependencies.decorators import requires_pillow, requires_pypdfium2
from mindee.error.mindee_error import MindeeError
from mindee.input.local_input_source import LocalInputSource
from mindee.pdf.extracted_pdf import ExtractedPDF

if PYPDFIUM2_AVAILABLE:
    # pylint: disable=import-error
    import pypdfium2 as pdfium
else:
    pdfium = None  # pylint: disable=invalid-name

if PILLOW_AVAILABLE:
    # pylint: disable=import-error
    from PIL import Image
else:
    Image: Any = None  # type: ignore[no-redef] # pylint: disable=invalid-name


class PDFExtractor:
    """PDF extraction class."""

    _source_pdf: BinaryIO
    _filename: str

    @requires_pillow
    def __init__(self, local_input: LocalInputSource):
        self._filename = local_input.filename
        if local_input.is_pdf():
            self._source_pdf = local_input.file_object
        else:
            pdf_image = Image.open(local_input.file_object)
            self._source_pdf = io.BytesIO()
            pdf_image.save(self._source_pdf, format="PDF")

    @requires_pypdfium2
    def get_page_count(self) -> int:
        """Get the number of pages in the PDF file."""
        pdf = pdfium.PdfDocument(self._source_pdf)
        return len(pdf)

    @requires_pypdfium2
    def cut_pages(self, page_indexes: list) -> BinaryIO:
        """
        Create a new PDF from pages and save it into a buffer.

        :param page_indexes: List of pages number to use for merging in the original PDF.
        :return: The buffer containing the new PDF.
        """
        self._source_pdf.seek(0)
        new_pdf = pdfium.PdfDocument.new()
        pdf = pdfium.PdfDocument(self._source_pdf)
        new_pdf.import_pages(pdf, page_indexes)
        bytes_io = io.BytesIO()
        new_pdf.save(bytes_io)
        return bytes_io

    @requires_pypdfium2
    def extract_sub_documents(
        self, page_indexes: list[list[int]]
    ) -> list[ExtractedPDF]:
        """
        Extract the sub-documents from the main pdf, based on the given list of page indexes.

        :param page_indexes: 2D list of numbers, representing page indexes.
        :return: A list of created PDFS.
        """
        extracted_pdfs: list[ExtractedPDF] = []
        extension = Path(self._filename).suffix
        stem = Path(self._filename).stem
        for page_index_elem in page_indexes:
            if not page_index_elem or len(page_index_elem) == 0:
                raise MindeeError("Empty indexes aren't allowed for extraction.")
            for page_index in page_index_elem:
                if page_index > self.get_page_count():
                    raise MindeeError(f"Index {page_index} is out of range.")
            first_page = page_index_elem[0]
            last_page = page_index_elem[len(page_index_elem) - 1]
            extracted_pdf = ExtractedPDF(
                self.cut_pages(page_index_elem),
                f"{stem}_pages-{(first_page + 1):03d}-{(last_page + 1):03d}{extension}",
                (first_page, last_page),
            )
            extracted_pdfs.append(extracted_pdf)
        return extracted_pdfs

    def extract_documents(
        self,
        page_indexes: list[list[int]],
    ) -> list[ExtractedPDF]:
        """
        Extracts complete PDFs from the document.

        :param page_indexes: List of sub-lists of pages to keep.
        :return: A list of extracted invoices.
        """
        if len(page_indexes) < 1:
            raise MindeeError("No indexes provided.")
        return self.extract_sub_documents(page_indexes)
