from mindee.parsing.common.string_dict import StringDict


class RawText:
    """Raw text extracted from the document."""

    page: int
    """Page the raw text was found on."""
    content: str
    """Content of the raw text."""

    def __init__(self, raw_response: StringDict):
        self.page = raw_response["page"]
        self.content = raw_response["content"]
