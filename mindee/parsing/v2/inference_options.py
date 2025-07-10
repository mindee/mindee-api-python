from typing import List

from mindee.parsing.common.string_dict import StringDict


class RawText:
    """Raw text extracted from the document."""

    page: int
    content: str

    def __init__(self, raw_response: StringDict):
        self.page = raw_response["page"]
        self.content = raw_response["content"]


class InferenceOptions:
    """Optional information about the document."""

    raw_texts: List[RawText]

    def __init__(self, raw_response: StringDict):
        self.raw_texts = [RawText(raw_text) for raw_text in raw_response["raw_texts"]]
