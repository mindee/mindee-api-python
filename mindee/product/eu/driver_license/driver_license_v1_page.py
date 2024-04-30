from typing import Optional

from mindee.parsing.common import StringDict, clean_out_string
from mindee.parsing.standard import PositionField
from mindee.product.eu.driver_license.driver_license_v1_document import (
    DriverLicenseV1Document,
)


class DriverLicenseV1Page(DriverLicenseV1Document):
    """Driver License API version 1.0 page data."""

    photo: PositionField
    """Has a photo of the EU driver license holder"""
    signature: PositionField
    """Has a signature of the EU driver license holder"""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Driver License page.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction=raw_prediction, page_id=page_id)
        self.photo = PositionField(
            raw_prediction["photo"],
            page_id=page_id,
        )
        self.signature = PositionField(
            raw_prediction["signature"],
            page_id=page_id,
        )

    def __str__(self) -> str:
        out_str: str = f":Photo: {self.photo}\n"
        out_str += f":Signature: {self.signature}\n"
        out_str += f"{super().__str__()}"
        return clean_out_string(out_str)
