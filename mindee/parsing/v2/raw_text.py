from typing import List

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.raw_text_page import RawTextPage


class RawText:
    """Raw text extracted from the document."""

    pages: List[RawTextPage]
    """Page the raw text was found on."""

    def __init__(self, raw_response: StringDict):
        self.pages = [RawTextPage(page) for page in raw_response.get("pages", [])]

    def __str__(self) -> str:
        return "\n\n".join([page.content for page in self.pages])
