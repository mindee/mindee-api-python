from typing import List

from mindee.extraction.pdf_extractor.extracted_pdf import ExtractedPdf
from mindee.extraction.pdf_extractor.pdf_extractor import PdfExtractor
from mindee.input.sources.local_input_source import LocalInputSource
from mindee.parsing.common.string_dict import StringDict


class SplitRange:
    """Split inference result."""

    page_range: List[int]
    """
    0-based page indexes, where the first integer indicates the start page and the
    second integer indicates the end page.
    """
    document_type: str
    """The document type, as identified on given classification values."""

    def __init__(self, server_response: StringDict):
        self.page_range = server_response["page_range"]
        self.document_type = server_response["document_type"]

    def __str__(self) -> str:
        page_range = ",".join([str(page_index) for page_index in self.page_range])
        return f"* :Page Range: {page_range}\n  :Document Type: {self.document_type}"

    def apply_to_file(self, input_source: LocalInputSource) -> ExtractedPdf:
        """
        Apply the split range inference to a file and return a single extracted PDF.

        :param input_source: Local file to apply the inference to
        :return: Extracted PDF
        """
        pdf_extractor = PdfExtractor(input_source)
        return pdf_extractor.extract_sub_documents([self.page_range])[0]
