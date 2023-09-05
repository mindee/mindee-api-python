from typing import List, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.text import TextField


class LicensePlateV1(Document):
    """License Plate v1 prediction results."""

    license_plates: List[TextField]
    """List of all license plates found in the image."""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        """
        License Plate v1 prediction results.

        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type="license_plate",
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
        self.license_plates = [
            TextField(prediction, page_id=page_n)
            for prediction in api_prediction["license_plates"]
        ]

    def __str__(self) -> str:
        license_plates = f"\n { ' ' * 16 }".join(
            [str(item) for item in self.license_plates],
        )
        return clean_out_string(
            "EU License Plate V1 Prediction\n"
            "==============================\n"
            f":Filename: {self.filename or ''}\n"
            f":License Plates: {license_plates}\n"
        )


TypeLicensePlateV1 = TypeVar(
    "TypeLicensePlateV1",
    bound=LicensePlateV1,
)
