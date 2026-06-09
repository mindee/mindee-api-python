from mindee.parsing.common.string_dict import StringDict


class RawTextPage:
    """Raw text extracted from the page."""

    content: str
    """Content of the raw text."""

    def __init__(self, raw_response: StringDict):
        self.content = raw_response["content"]
