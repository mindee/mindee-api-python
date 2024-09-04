from typing import Optional

from mindee.parsing.common.string_dict import StringDict


class FullTextOcrExtra:
    """Full Text OCR result."""

    content: Optional[str]
    language: Optional[str]

    def __init__(self, raw_prediction: StringDict) -> None:
        if raw_prediction and "content" in raw_prediction:
            self.content = raw_prediction["content"]

        if raw_prediction and "language" in raw_prediction:
            self.language = raw_prediction["language"]

    def __str__(self) -> str:
        return self.content if self.content else ""
