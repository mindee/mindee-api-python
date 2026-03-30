from typing import List, Union

from mindee.error import MindeeError
from mindee.extraction import PdfExtractor
from mindee.input.sources.local_input_source import LocalInputSource
from mindee.v2.file_operations.split_files import SplitFiles
from mindee.v2.product.split.split_range import SplitRange


def extract_splits(
    input_source: LocalInputSource,
    splits: Union[List[SplitRange], List[List[int]]],
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
        if isinstance(split, SplitRange):
            lower_bound = split.page_range[0]
            upper_bound = split.page_range[1]
        else:
            lower_bound = split[0]
            upper_bound = split[1]
        page_groups.append(list(range(lower_bound, upper_bound + 1)))
    if len(splits) < 1:
        raise MindeeError("No indexes provided.")
    return SplitFiles(pdf_extractor.extract_sub_documents(page_groups))
