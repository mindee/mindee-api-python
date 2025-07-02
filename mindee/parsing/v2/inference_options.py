from typing import List, Optional

from mindee.parsing.common.string_dict import StringDict


class InferenceOptions:
    """Optional information about the document."""

    raw_text: Optional[List[str]]

    def __init__(self, raw_response: StringDict):
        self.raw_text = raw_response["raw_text"] if "raw_text" in raw_response else None
