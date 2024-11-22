from typing import List, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.position import PositionField
from mindee.product.us.bank_check.bank_check_v1_document import (
    BankCheckV1Document,
)


class BankCheckV1Page(BankCheckV1Document):
    """Bank Check API version 1.1 page data."""

    check_position: PositionField
    """The position of the check on the document."""
    signatures_positions: List[PositionField]
    """List of signature positions"""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Bank Check page.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction=raw_prediction, page_id=page_id)
        self.check_position = PositionField(
            raw_prediction["check_position"],
            page_id=page_id,
        )
        self.signatures_positions = [
            PositionField(prediction, page_id=page_id)
            for prediction in raw_prediction["signatures_positions"]
        ]

    def __str__(self) -> str:
        signatures_positions = f"\n { ' ' * 21 }".join(
            [str(item) for item in self.signatures_positions],
        )
        out_str: str = f":Check Position: {self.check_position}\n"
        out_str += f":Signature Positions: {signatures_positions}\n"
        out_str += f"{super().__str__()}"
        return clean_out_string(out_str)
