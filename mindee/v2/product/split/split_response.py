from typing import List

from mindee.extraction import ExtractedPdf
from mindee.input.sources.local_input_source import LocalInputSource
from mindee.parsing.common.string_dict import StringDict
from mindee.v2.file_operations.split import Split
from mindee.v2.parsing.inference import BaseResponse
from mindee.v2.product.split.split_inference import SplitInference


class SplitResponse(BaseResponse):
    """Represent a split inference response from Mindee V2 API."""

    inference: SplitInference
    """Inference object for split inference."""

    _slug: str = "products/split/results"
    """Slug of the inference."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.inference = SplitInference(raw_response["inference"])

    def apply_to_file(self, input_source: LocalInputSource) -> List[ExtractedPdf]:
        """
        Apply the split inference to a file and return a list of extracted PDFs.

        :param input_source: Local file to apply the inference to
        :return: List of extracted PDFs
        """
        return Split.extract_splits(input_source, self.inference.result.splits)
