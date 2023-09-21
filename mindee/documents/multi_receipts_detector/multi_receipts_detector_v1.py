from typing import List, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.position import PositionField


class MultiReceiptsDetectorV1(Document):
    """Multi Receipts Detector v1 prediction results."""

    receipts: List[PositionField]
    """Positions of the receipts on the document."""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        """
        Multi Receipts Detector v1 prediction results.

        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type="multi_receipts_detector",
            api_prediction=api_prediction,
            page_n=page_n,
        )
        self._build_from_api_prediction(api_prediction["prediction"], page_n=page_n)

    def _build_from_api_prediction(
        self, api_prediction: TypeApiPrediction, page_n: Optional[int] = None
    ) -> None:
        """
        Build the object from the prediction API JSON.

        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number
        """
        self.receipts = [
            PositionField(prediction, page_id=page_n)
            for prediction in api_prediction["receipts"]
        ]

    def __str__(self) -> str:
        receipts = f"\n { ' ' * 18 }".join(
            [str(item) for item in self.receipts],
        )
        return clean_out_string(
            "Multi Receipts Detector V1 Prediction\n"
            "=====================================\n"
            f":Filename: {self.filename or ''}\n"
            f":List of Receipts: {receipts}\n"
        )


TypeMultiReceiptsDetectorV1 = TypeVar(
    "TypeMultiReceiptsDetectorV1",
    bound=MultiReceiptsDetectorV1,
)
