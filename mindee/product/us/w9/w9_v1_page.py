from typing import Optional

from mindee.parsing.common import StringDict, clean_out_string
from mindee.parsing.standard import PositionField, StringField
from mindee.product.us.w9.w9_v1_document import (
    W9V1Document,
)


class W9V1Page(W9V1Document):
    """W9 API version 1.0 page data."""

    address: StringField
    """The street address (number, street, and apt. or suite no.) of the applicant."""
    business_name: StringField
    """The business name or disregarded entity name, if different from Name."""
    city_state_zip: StringField
    """The city, state, and ZIP code of the applicant."""
    ein: StringField
    """The employer identification number."""
    name: StringField
    """Name as shown on the applicant's income tax return."""
    signature_date_position: PositionField
    """Position of the signature date on the document."""
    signature_position: PositionField
    """Position of the signature on the document."""
    ssn: StringField
    """The applicant's social security number."""
    tax_classification: StringField
    """The federal tax classification, which can vary depending on the revision date."""
    tax_classification_llc: StringField
    """Depending on revision year, among S, C, P or D for Limited Liability Company Classification."""
    tax_classification_other_details: StringField
    """Tax Classification Other Details."""
    w9_revision_date: StringField
    """The Revision month and year of the W9 form."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        W9 page.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction=raw_prediction, page_id=page_id)
        self.address = StringField(
            raw_prediction["address"],
            page_id=page_id,
        )
        self.business_name = StringField(
            raw_prediction["business_name"],
            page_id=page_id,
        )
        self.city_state_zip = StringField(
            raw_prediction["city_state_zip"],
            page_id=page_id,
        )
        self.ein = StringField(
            raw_prediction["ein"],
            page_id=page_id,
        )
        self.name = StringField(
            raw_prediction["name"],
            page_id=page_id,
        )
        self.signature_date_position = PositionField(
            raw_prediction["signature_date_position"],
            page_id=page_id,
        )
        self.signature_position = PositionField(
            raw_prediction["signature_position"],
            page_id=page_id,
        )
        self.ssn = StringField(
            raw_prediction["ssn"],
            page_id=page_id,
        )
        self.tax_classification = StringField(
            raw_prediction["tax_classification"],
            page_id=page_id,
        )
        self.tax_classification_llc = StringField(
            raw_prediction["tax_classification_llc"],
            page_id=page_id,
        )
        self.tax_classification_other_details = StringField(
            raw_prediction["tax_classification_other_details"],
            page_id=page_id,
        )
        self.w9_revision_date = StringField(
            raw_prediction["w9_revision_date"],
            page_id=page_id,
        )

    def __str__(self) -> str:
        out_str: str = f":Name: {self.name}\n"
        out_str += f":SSN: {self.ssn}\n"
        out_str += f":Address: {self.address}\n"
        out_str += f":City State Zip: {self.city_state_zip}\n"
        out_str += f":Business Name: {self.business_name}\n"
        out_str += f":EIN: {self.ein}\n"
        out_str += f":Tax Classification: {self.tax_classification}\n"
        out_str += f":Tax Classification Other Details: {self.tax_classification_other_details}\n"
        out_str += f":W9 Revision Date: {self.w9_revision_date}\n"
        out_str += f":Signature Position: {self.signature_position}\n"
        out_str += f":Signature Date Position: {self.signature_date_position}\n"
        out_str += f":Tax Classification LLC: {self.tax_classification_llc}\n"
        out_str += f"{super().__str__()}"
        return clean_out_string(out_str)
