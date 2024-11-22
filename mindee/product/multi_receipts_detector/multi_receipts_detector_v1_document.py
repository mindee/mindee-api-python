from typing import List, Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.position import PositionField


class MultiReceiptsDetectorV1Document(Prediction):
    """Multi Receipts Detector API version 1.1 document data."""

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
        super().__init__(raw_prediction, page_id)
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
