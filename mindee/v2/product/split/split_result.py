from mindee.input.local_input_source import LocalInputSource
from mindee.parsing.common.string_dict import StringDict
from mindee.pdf.extracted_pdfs import ExtractedPDFs
from mindee.v2.file_operations.split import extract_multiple_splits
from mindee.v2.product.split.split_range import SplitRange


class SplitResult:
    """Split result info."""

    splits: list[SplitRange]

    def __init__(self, raw_response: StringDict) -> None:
        self.splits = [SplitRange(split) for split in raw_response["splits"]]

    def __str__(self) -> str:
        splits = "\n"
        if len(self.splits) > 0:
            splits += "\n\n".join([str(split) for split in self.splits])
        out_str = f"Splits\n======{splits}"
        return out_str

    def extract_from_input_source(
        self, input_source: LocalInputSource
    ) -> ExtractedPDFs:
        """
        Apply all the crops to a file and return a single extracted PDF.

        :param input_source: Input file
        """
        return extract_multiple_splits(
            input_source, [split.page_range for split in self.splits]
        )
