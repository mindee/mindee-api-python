from typing import List

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.raw_text import RawText


class InferenceResultOptions:
    """Optional information about the document."""

    raw_texts: List[RawText]
    """List of text found per page."""

    def __init__(self, raw_response: StringDict):
        self.raw_texts = [RawText(raw_text) for raw_text in raw_response["raw_texts"]]
