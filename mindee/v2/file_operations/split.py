from typing import List, Union

from mindee.error import MindeeError
from mindee.extraction import ExtractedPdf, PdfExtractor
from mindee.input.sources.local_input_source import LocalInputSource
from mindee.v2.product.split.split_range import SplitRange


class Split:
    """Split operations for V2."""

    @classmethod
    def extract_splits(
        cls,
        input_source: LocalInputSource,
        splits: Union[List[SplitRange], List[List[int]]],
    ) -> List[ExtractedPdf]:
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
                page_groups.append(split.page_range)
            else:
                page_groups.append(split)
        if len(splits) < 1:
            raise MindeeError("No indexes provided.")
        return pdf_extractor.extract_sub_documents(page_groups)

    @classmethod
    def apply(
        cls, input_source: LocalInputSource, splits: List[SplitRange]
    ) -> List[ExtractedPdf]:
        """Split a document into multiple pages.

        :param input_source: Input source to split.
        :param splits: List of splits.
        """

        return cls.extract_splits(input_source, splits)
