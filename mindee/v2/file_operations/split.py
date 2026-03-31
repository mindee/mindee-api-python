from typing import List, Union

from mindee.error import MindeeError
from mindee.extraction.pdf_extractor.extracted_pdf import ExtractedPdf
from mindee.extraction.pdf_extractor.pdf_extractor import PdfExtractor
from mindee.input.sources.local_input_source import LocalInputSource
from mindee.v2.file_operations.split_files import SplitFiles


def extract_single_split(
    input_source: LocalInputSource, split: List[int]
) -> ExtractedPdf:
    """
    Extracts a single split as a complete PDF from the document.

    :param input_source: Input source to split.
    :param split: List of pages to keep.
    :return: Extracted PDF
    """
    return extract_splits(input_source, [split])[0]


def extract_splits(
    input_source: LocalInputSource,
    splits: Union[List[List[int]]],
) -> SplitFiles:
    """
    Extracts splits as complete PDFs from the document.

    :param input_source: Input source to split.
    :param splits: List of sub-lists of pages to keep.
    :return: A list of extracted invoices.
    """
    pdf_extractor = PdfExtractor(input_source)
    page_groups = []
    for split in splits:
        page_groups.append(list(range(split[0], split[1] + 1)))
    if len(splits) < 1:
        raise MindeeError("No indexes provided.")
    return SplitFiles(pdf_extractor.extract_sub_documents(page_groups))
