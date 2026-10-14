from __future__ import annotations

import io
from pathlib import Path
from typing import BinaryIO

from mindee.dependencies.checkers import BERNARD_LEDIT_AVAILABLE
from mindee.dependencies.decorators import requires_bernard_ledit
from mindee.error.mindee_error import MindeeError
from mindee.input.local_input_source import LocalInputSource
from mindee.pdf.extracted_pdf import ExtractedPDF
from mindee.pdf.extracted_pdfs import ExtractedPDFs

if BERNARD_LEDIT_AVAILABLE:
    # pylint: disable=import-error
    import bernard_ledit.pdf as bernard_pdf
else:
    bernard_pdf = None  # type: ignore[assignment]  # pylint: disable=invalid-name


class PDFExtractor:
    """PDF extraction class."""

    _source: BinaryIO
    _filename: str
    _page_count: int

    @requires_bernard_ledit
    def __init__(self, local_input: LocalInputSource):
        self._filename = local_input.filename
        self._page_count = local_input.page_count
        self._source = local_input.file_object

    @requires_bernard_ledit
    def extract_single_document(self, page_indexes: list[int]) -> ExtractedPDF:
        """
        Create a new PDF from pages and save it into a buffer.

        :param page_indexes: List of pages number to use for merging in the original PDF.
        :return: The buffer containing the new PDF.
        """

        if not page_indexes or len(page_indexes) == 0:
            raise MindeeError("Empty indexes aren't allowed for extraction.")
        self._check_indexes(page_indexes)
        return self._extract([page_indexes])[0]

    @requires_bernard_ledit
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
        for group in page_indexes:
            if not group:
                raise MindeeError("Empty indexes aren't allowed for extraction.")
            self._check_indexes(group)
        return ExtractedPDFs(self._extract(page_indexes))

    def _check_indexes(self, page_indexes: list[int]) -> None:
        for page_index in page_indexes:
            if page_index < 0 or page_index >= self._page_count:
                raise MindeeError(f"Index {page_index} is out of range.")

    def _extract(self, groups: list[list[int]]) -> list[ExtractedPDF]:
        self._source.seek(0)
        docs = bernard_pdf.extract_documents(self._source, groups)  # type: ignore[attr-defined]
        extracted: list[ExtractedPDF] = []
        for doc, indexes in zip(docs, groups, strict=True):
            with doc:
                bytes_io = io.BytesIO()
                doc.save(bytes_io)
            extracted.append(
                ExtractedPDF(
                    pdf_byte_stream=bytes_io,
                    filename=self._make_filename(indexes[0], indexes[-1]),
                    page_indexes=indexes,
                )
            )
        return extracted

    def _make_filename(self, first_page: int, last_page: int) -> str:
        stem = Path(self._filename).stem
        return f"{stem}_pages-{(first_page + 1):03d}-{(last_page + 1):03d}.pdf"
