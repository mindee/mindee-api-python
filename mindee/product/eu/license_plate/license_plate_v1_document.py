from typing import List, Optional

from mindee.parsing.common import Prediction, StringDict, clean_out_string
from mindee.parsing.standard import StringField


class LicensePlateV1Document(Prediction):
    """License Plate API version 1.1 document data."""

    license_plates: List[StringField]
    """List of all license plates found in the image."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        License Plate document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction, page_id)
        self.license_plates = [
            StringField(prediction, page_id=page_id)
            for prediction in raw_prediction["license_plates"]
        ]

    def __str__(self) -> str:
        license_plates = f"\n { ' ' * 16 }".join(
            [str(item) for item in self.license_plates],
        )
        out_str: str = f":License Plates: {license_plates}\n"
        return clean_out_string(out_str)
