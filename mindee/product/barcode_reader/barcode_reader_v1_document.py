from typing import List, Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.text import StringField


class BarcodeReaderV1Document(Prediction):
    """Barcode Reader API version 1.0 document data."""

    codes_1d: List[StringField]
    """List of decoded 1D barcodes."""
    codes_2d: List[StringField]
    """List of decoded 2D barcodes."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Barcode Reader document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction, page_id)
        self.codes_1d = [
            StringField(prediction, page_id=page_id)
            for prediction in raw_prediction["codes_1d"]
        ]
        self.codes_2d = [
            StringField(prediction, page_id=page_id)
            for prediction in raw_prediction["codes_2d"]
        ]

    def __str__(self) -> str:
        codes_1d = f"\n { ' ' * 13 }".join(
            [str(item) for item in self.codes_1d],
        )
        codes_2d = f"\n { ' ' * 13 }".join(
            [str(item) for item in self.codes_2d],
        )
        out_str: str = f":Barcodes 1D: {codes_1d}\n"
        out_str += f":Barcodes 2D: {codes_2d}\n"
        return clean_out_string(out_str)
