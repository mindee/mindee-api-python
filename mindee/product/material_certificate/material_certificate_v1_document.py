from typing import Optional

from mindee.parsing.common import Prediction, StringDict, clean_out_string
from mindee.parsing.standard import StringField


class MaterialCertificateV1Document(Prediction):
    """Document data for Material Certificate, API version 1."""

    certificate_type: StringField
    """The type of certification."""
    heat_number: StringField
    """Heat Number is a unique identifier assigned to a batch of material produced in a manufacturing process."""
    norm: StringField
    """The international standard used for certification."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Material Certificate document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        self.certificate_type = StringField(
            raw_prediction["certificate_type"],
            page_id=page_id,
        )
        self.heat_number = StringField(
            raw_prediction["heat_number"],
            page_id=page_id,
        )
        self.norm = StringField(
            raw_prediction["norm"],
            page_id=page_id,
        )

    def __str__(self) -> str:
        out_str: str = f":Certificate Type: {self.certificate_type}\n"
        out_str += f":Norm: {self.norm}\n"
        out_str += f":Heat Number: {self.heat_number}\n"
        return clean_out_string(out_str)
