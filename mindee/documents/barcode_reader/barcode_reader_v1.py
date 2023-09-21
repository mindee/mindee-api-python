from typing import List, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.text import TextField


class BarcodeReaderV1(Document):
    """Barcode Reader v1 prediction results."""

    codes_1d: List[TextField]
    """List of decoded 1D barcodes."""
    codes_2d: List[TextField]
    """List of decoded 2D barcodes."""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        """
        Barcode Reader v1 prediction results.

        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type="barcode_reader",
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
        self.codes_1d = [
            TextField(prediction, page_id=page_n)
            for prediction in api_prediction["codes_1d"]
        ]
        self.codes_2d = [
            TextField(prediction, page_id=page_n)
            for prediction in api_prediction["codes_2d"]
        ]

    def __str__(self) -> str:
        codes_1d = f"\n { ' ' * 13 }".join(
            [str(item) for item in self.codes_1d],
        )
        codes_2d = f"\n { ' ' * 13 }".join(
            [str(item) for item in self.codes_2d],
        )
        return clean_out_string(
            "Barcode Reader V1 Prediction\n"
            "============================\n"
            f":Filename: {self.filename or ''}\n"
            f":Barcodes 1D: {codes_1d}\n"
            f":Barcodes 2D: {codes_2d}\n"
        )


TypeBarcodeReaderV1 = TypeVar(
    "TypeBarcodeReaderV1",
    bound=BarcodeReaderV1,
)
