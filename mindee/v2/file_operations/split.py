from mindee.error import MindeeError
from mindee.input.local_input_source import LocalInputSource
from mindee.pdf.extracted_pdf import ExtractedPDF
from mindee.pdf.extracted_pdfs import ExtractedPDFs
from mindee.pdf.pdf_extractor import PDFExtractor


def extract_single_split(
    input_source: LocalInputSource, split: list[int]
) -> ExtractedPDF:
    """
    Extracts a single split as a complete PDF from the document.

    :param input_source: Input source to split.
    :param split: List of pages to keep.
    :return: Extracted PDF
    """
    return extract_multiple_splits(input_source, [split])[0]


def extract_multiple_splits(
    input_source: LocalInputSource,
    splits: list[list[int]],
) -> ExtractedPDFs:
    """
    Extracts splits as complete PDFs from the document.

    :param input_source: Input source to split.
    :param splits: List of sub-lists of pages to keep.
    :return: A list of extracted invoices.
    """
    pdf_extractor = PDFExtractor(input_source)
    page_groups = []
    for split in splits:
        page_groups.append(list(range(split[0], split[1] + 1)))
    if len(splits) < 1:
        raise MindeeError("No indexes provided.")
    return ExtractedPDFs(pdf_extractor.extract_sub_documents(page_groups))
