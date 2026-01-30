from typing import List

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.product.split.split_split import SplitSplit


class SplitResult:
    """Split result info."""

    split: List[SplitSplit]

    def __init__(self, raw_response: StringDict) -> None:
        self.split = [SplitSplit(split) for split in raw_response["split"]]

    def __str__(self) -> str:
        splits = "\n"
        if len(self.split) > 0:
            splits += "\n\n".join([str(split) for split in self.split])
        out_str = f"Splits\n======{splits}"
        return out_str
