from mindee.error import MindeeError
from mindee.pdf.extracted_pdf import ExtractedPDF
from mindee.pdf.pdf_extractor import PDFExtractor as BasePDFExtractor
from mindee.v1.product import InvoiceSplitterV1InvoicePageGroup


class PDFExtractor(BasePDFExtractor):
    """V1-specific PDF extractor."""

    def extract_invoices(
        self,
        page_indexes: list[InvoiceSplitterV1InvoicePageGroup | list[int]],
        strict: bool = False,
    ) -> list[ExtractedPDF]:
        """
        Extracts invoices as complete PDFs from the document from either a list of pages
        or a list of page groups.

        :param page_indexes: List of sub-lists of pages to keep.
        :param strict: Whether to trust confidence scores above 0.5 (included) or not.
        :return: A list of extracted invoices.
        """

        if len(page_indexes) < 1:
            raise MindeeError("No indexes provided.")
        if not isinstance(page_indexes[0], InvoiceSplitterV1InvoicePageGroup):
            return self.extract_multiple_documents(page_indexes)  # type: ignore

        if not strict:
            indexes_as_list = [page_index.page_indexes for page_index in page_indexes]  # type: ignore
            return self.extract_multiple_documents(indexes_as_list)
        correct_page_indexes: list[list[int]] = []
        current_list: list[int] = []
        previous_confidence: float | None = None
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
        return self.extract_multiple_documents(correct_page_indexes)
