import io
from pathlib import Path
from typing import BinaryIO, List, Optional, Union

import pypdfium2 as pdfium
from PIL import Image

from mindee.error.mindee_error import MindeeError
from mindee.extraction.pdf_extractor.extracted_pdf import ExtractedPdf
from mindee.input.sources.local_input_source import LocalInputSource
from mindee.product.invoice_splitter import InvoiceSplitterV1InvoicePageGroup


class PdfExtractor:
    """PDF extraction class."""

    _source_pdf: BinaryIO
    _filename: str

    def __init__(self, local_input: LocalInputSource):
        self._filename = local_input.filename
        if local_input.is_pdf():
            self._source_pdf = local_input.file_object
        else:
            pdf_image = Image.open(local_input.file_object)
            self._source_pdf = io.BytesIO()
            pdf_image.save(self._source_pdf, format="PDF")

    def get_page_count(self) -> int:
        """Get the number of pages in the PDF file."""
        pdf = pdfium.PdfDocument(self._source_pdf)
        return len(pdf)

    def cut_pages(self, page_indexes: List) -> BinaryIO:
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

    def extract_sub_documents(
        self, page_indexes: List[List[int]]
    ) -> List[ExtractedPdf]:
        """
        Extract the sub-documents from the main pdf, based on the given list of page indexes.

        :param page_indexes: List of list of numbers, representing page indexes.
        :return: A list of created PDFS.
        """
        extracted_pdfs: List[ExtractedPdf] = []
        extension = Path(self._filename).suffix
        stem = Path(self._filename).stem
        for page_index_elem in page_indexes:
            if not page_index_elem or len(page_index_elem) == 0:
                raise MindeeError("Empty indexes aren't allowed for extraction.")
            for page_index in page_index_elem:
                if page_index > self.get_page_count():
                    raise MindeeError(f"Index {page_index} is out of range.")
            formatted_max_index = f"{page_index_elem[len(page_index_elem) - 1] + 1:03d}"
            field_filename = f"{stem}_{(page_index_elem[0] + 1):03d}-{formatted_max_index}{extension}"
            extracted_pdf = ExtractedPdf(
                self.cut_pages(page_index_elem), field_filename
            )
            extracted_pdfs.append(extracted_pdf)
        return extracted_pdfs

    def extract_invoices(
        self,
        page_indexes: List[Union[InvoiceSplitterV1InvoicePageGroup, List[int]]],
        strict: bool = False,
    ) -> List[ExtractedPdf]:
        """
        Extracts invoices as complete PDFs from the document.

        :param page_indexes: List of sub-lists of pages to keep.
        :param strict: Whether to trust confidence scores above 0.5 (included) or not.
        :return: A list of extracted invoices.
        """
        if len(page_indexes) < 1:
            raise MindeeError("No indexes provided.")
        if not isinstance(page_indexes[0], InvoiceSplitterV1InvoicePageGroup):
            return self.extract_sub_documents(page_indexes)  # type: ignore
        if not strict:
            indexes_as_list = [page_index.page_indexes for page_index in page_indexes]  # type: ignore
            return self.extract_sub_documents(indexes_as_list)
        correct_page_indexes: List[List[int]] = []
        current_list: List[int] = []
        previous_confidence: Optional[float] = None
        for i, page_index in enumerate(page_indexes):
            assert isinstance(page_index, InvoiceSplitterV1InvoicePageGroup)
            confidence = page_index.confidence
            page_list = page_index.page_indexes

            if confidence >= 0.5 and previous_confidence is None:
                current_list = page_list
            elif confidence >= 0.5 and i != len(page_indexes) - 1:
                correct_page_indexes.append(current_list)
                current_list = page_list
            elif confidence < 0.5 and i == len(page_indexes) - 1:
                current_list.extend(page_list)
                correct_page_indexes.append(current_list)
            else:
                correct_page_indexes.append(current_list)
                correct_page_indexes.append(page_list)
            previous_confidence = confidence
        return self.extract_sub_documents(correct_page_indexes)
