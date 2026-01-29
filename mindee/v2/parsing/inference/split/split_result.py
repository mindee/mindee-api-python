from typing import List

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference.split.split import Split


class SplitResult:
    """Split result info."""

    split: List[Split]

    def __init__(self, raw_response: StringDict) -> None:
        self.split = [Split(split) for split in raw_response["split"]]

    def __str__(self) -> str:
        out_str = f"Splits\n======{self.split}"
        return out_str
