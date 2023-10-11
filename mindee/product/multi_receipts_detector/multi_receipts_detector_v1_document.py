from typing import List, Optional

from mindee.parsing.common import Prediction, StringDict, clean_out_string
from mindee.parsing.standard import PositionField


class MultiReceiptsDetectorV1Document(Prediction):
    """Document data for Multi Receipts Detector, API version 1."""

    receipts: List[PositionField]
    """Positions of the receipts on the document."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Multi Receipts Detector document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        self.receipts = [
            PositionField(prediction, page_id=page_id)
            for prediction in raw_prediction["receipts"]
        ]

    def __str__(self) -> str:
        receipts = f"\n { ' ' * 18 }".join(
            [str(item) for item in self.receipts],
        )
        out_str: str = f":List of Receipts: {receipts}\n"
        return clean_out_string(out_str)
