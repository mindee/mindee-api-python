from typing import Optional

from mindee.parsing.common import StringDict, clean_out_string
from mindee.product.us.driver_license.driver_license_v1_document import (
    DriverLicenseV1Document,
)

from mindee.parsing.standard import PositionField


class DriverLicenseV1Page(DriverLicenseV1Document):
    """Page data for Driver License, API version 1."""

    photo: PositionField
    """Has a photo of the US driver license holder"""
    signature: PositionField
    """Has a signature of the US driver license holder"""

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
        return clean_out_string(
            f":Photo: {self.photo}\n" f":Signature: {self.signature}\n" + f"{super().__str__()}"
        )
