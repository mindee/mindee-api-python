from typing import List

from mindee.parsing.common.string_dict import StringDict


class InferenceOptions:
    """Optional information about the document."""

    raw_text: List[str]

    def __init__(self, raw_response: StringDict):
        self.raw_text = raw_response["raw_text"]
