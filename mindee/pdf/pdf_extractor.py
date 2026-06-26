from __future__ import annotations

import io
from pathlib import Path
from typing import Any, BinaryIO

from mindee.dependencies.checkers import PILLOW_AVAILABLE, PYPDFIUM2_AVAILABLE
from mindee.dependencies.decorators import requires_pillow, requires_pypdfium2
from mindee.error.mindee_error import MindeeError
from mindee.input.local_input_source import LocalInputSource
from mindee.pdf.extracted_pdf import ExtractedPDF
from mindee.pdf.extracted_pdfs import ExtractedPDFs

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
    _page_count: int

    @requires_pillow
    def __init__(self, local_input: LocalInputSource):
        self._filename = local_input.filename
        self._page_count = local_input.page_count
        if local_input.is_pdf():
            self._source_pdf = local_input.file_object
        else:
            pdf_image = Image.open(local_input.file_object)
            self._source_pdf = io.BytesIO()
            pdf_image.save(self._source_pdf, format="PDF")

    @requires_pypdfium2
    def extract_single_document(self, page_indexes: list[int]) -> ExtractedPDF:
        """
        Create a new PDF from pages and save it into a buffer.

        :param page_indexes: List of pages number to use for merging in the original PDF.
        :return: The buffer containing the new PDF.
        """
        if not page_indexes or len(page_indexes) == 0:
            raise MindeeError("Empty indexes aren't allowed for extraction.")
        for page_index in page_indexes:
            if page_index > self._page_count:
                raise MindeeError(f"Index {page_index} is out of range.")

        self._source_pdf.seek(0)
        new_pdf = pdfium.PdfDocument.new()
        pdf = pdfium.PdfDocument(self._source_pdf)
        new_pdf.import_pages(pdf, page_indexes)
        bytes_io = io.BytesIO()
        new_pdf.save(bytes_io)

        first_page = page_indexes[0]
        last_page = page_indexes[len(page_indexes) - 1]
        return ExtractedPDF(
            pdf_byte_stream=bytes_io,
            filename=self._make_filename(first_page, last_page),
            page_indexes=page_indexes,
        )

    @requires_pypdfium2
    def extract_multiple_documents(
        self, page_indexes: list[list[int]]
    ) -> ExtractedPDFs:
        """
        Extract the sub-documents from the main pdf, based on the given list of page indexes.

        :param page_indexes: 2D list of numbers, representing page indexes.
        :return: A list of created PDFS.
        """
        if len(page_indexes) < 1:
            raise MindeeError("No indexes provided.")
        extracted_pdfs: list[ExtractedPDF] = []
        for page_index_elem in page_indexes:
            extracted_pdfs.append(self.extract_single_document(page_index_elem))
        return ExtractedPDFs(extracted_pdfs)

    def _make_filename(self, first_page: int, last_page: int) -> str:
        stem = Path(self._filename).stem
        return f"{stem}_pages-{(first_page + 1):03d}-{(last_page + 1):03d}.pdf"
