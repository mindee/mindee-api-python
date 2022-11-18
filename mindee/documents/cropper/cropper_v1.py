from typing import List, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.position import PositionField


class CropperV1(Document):
    cropping: List[PositionField]
    """List of all detected cropped elements in the image"""

    def __init__(
        self,
        api_prediction: TypeApiPrediction,
        input_source=None,
        page_n: Optional[int] = None,
        document_type="cropper",
    ):
        """
        Custom document object.

        :param document_type: Document type
        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type=document_type,
            api_prediction=api_prediction,
            page_n=page_n,
        )
        self._build_from_api_prediction(api_prediction["prediction"], page_n=page_n)

    def _build_from_api_prediction(
        self, api_prediction: TypeApiPrediction, page_n: Optional[int] = None
    ) -> None:
        """Build the document from an API response JSON."""
        self.cropping = []

        # cropping is only present on pages
        if page_n is None:
            return

        for crop in api_prediction["cropping"]:
            self.cropping.append(PositionField(prediction=crop))

    def _checklist(self) -> None:
        pass

    def __str__(self):
        cropping = "\n          ".join([str(crop) for crop in self.cropping])
        return clean_out_string(
            "----- Cropper Data -----\n"
            f"Filename: {self.filename or ''}\n"
            f"Cropping: {cropping}\n"
            "------------------------"
        )


TypeCropperV1 = TypeVar("TypeCropperV1", bound=CropperV1)
