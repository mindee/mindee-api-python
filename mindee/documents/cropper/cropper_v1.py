from typing import List, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.position import PositionField


class CropperV1(Document):
    """Cropper v1 prediction results."""

    cropping: List[PositionField] = []
    """List of documents found in the image."""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        """
        Cropper v1 prediction results.

        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type="cropper",
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
        if page_n is None:
            return

        self.cropping = [
            PositionField(prediction, page_id=page_n)
            for prediction in api_prediction["cropping"]
        ]

    def __str__(self) -> str:
        cropping = f"\n { ' ' * 18 }".join(
            [str(item) for item in self.cropping],
        )
        return clean_out_string(
            "Cropper V1 Prediction\n"
            "=====================\n"
            f":Filename: {self.filename or ''}\n"
            f":Document Cropper: {cropping}\n"
        )


TypeCropperV1 = TypeVar(
    "TypeCropperV1",
    bound=CropperV1,
)
