from typing import List

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.product.split.split_range import SplitRange


class SplitResult:
    """Split result info."""

    splits: List[SplitRange]

    def __init__(self, raw_response: StringDict) -> None:
        self.splits = [SplitRange(split) for split in raw_response["split"]]

    def __str__(self) -> str:
        splits = "\n"
        if len(self.splits) > 0:
            splits += "\n\n".join([str(split) for split in self.splits])
        out_str = f"Splits\n======{splits}"
        return out_str
