from mindee.input.local_input_source import LocalInputSource
from mindee.parsing.common.string_dict import StringDict
from mindee.pdf.extracted_pdf import ExtractedPDF
from mindee.v2.file_operations.split import extract_single_split
from mindee.v2.product.extraction.extraction_response import ExtractionResponse


class SplitRange:
    """Split inference result."""

    page_range: list[int]
    """
    0-based page indexes, where the first integer indicates the start page and the
    second integer indicates the end page.
    """

    document_type: str
    """The document type, as identified on given classification values."""

    extraction_response: ExtractionResponse | None = None
    """The extraction response associated with the split."""

    def __init__(self, server_response: StringDict):
        self.page_range = server_response["page_range"]
        self.document_type = server_response["document_type"]
        if server_response.get("extraction_response") is not None:
            self.extraction_response = ExtractionResponse(
                server_response["extraction_response"]
            )

    def __str__(self) -> str:
        page_range = ",".join([str(page_index) for page_index in self.page_range])
        return f"* :Page Range: {page_range}\n  :Document Type: {self.document_type}"

    def extract_from_input_source(self, input_source: LocalInputSource) -> ExtractedPDF:
        """
        Apply the split range inference to a file and return a single extracted PDF.

        :param input_source: Local file to apply the inference to
        :return: Extracted PDF
        """
        return extract_single_split(input_source, self.page_range)
