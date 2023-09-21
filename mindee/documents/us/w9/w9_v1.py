from typing import Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.position import PositionField
from mindee.fields.text import TextField


class W9V1(Document):
    """US W9 v1 prediction results."""

    address: TextField
    """The street address (number, street, and apt. or suite no.) of the applicant."""
    business_name: TextField
    """The business name or disregarded entity name, if different from Name."""
    city_state_zip: TextField
    """The city, state, and ZIP code of the applicant."""
    ein: TextField
    """The employer identification number."""
    name: TextField
    """Name as shown on the applicant's income tax return."""
    signature_date_position: PositionField
    """Position of the signature date on the document."""
    signature_position: PositionField
    """Position of the signature on the document."""
    ssn: TextField
    """The applicant's social security number."""
    tax_classification: TextField
    """The federal tax classification, which can vary depending on the revision date."""
    tax_classification_llc: TextField
    """Depending on revision year, among S, C, P or D for Limited Liability Company Classification."""
    tax_classification_other_details: TextField
    """Tax Classification Other Details."""
    w9_revision_date: TextField
    """The Revision month and year of the W9 form."""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        """
        US W9 v1 prediction results.

        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type="w9",
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
        self.address = TextField(
            api_prediction.get("address", {}),
            page_id=page_n,
        )
        self.business_name = TextField(
            api_prediction.get("business_name", {}),
            page_id=page_n,
        )
        self.city_state_zip = TextField(
            api_prediction.get("city_state_zip", {}),
            page_id=page_n,
        )
        self.ein = TextField(
            api_prediction.get("ein", {}),
            page_id=page_n,
        )
        self.name = TextField(
            api_prediction.get("name", {}),
            page_id=page_n,
        )
        self.signature_date_position = PositionField(
            api_prediction.get("signature_date_position", {}),
            page_id=page_n,
        )
        self.signature_position = PositionField(
            api_prediction.get("signature_position", {}),
            page_id=page_n,
        )
        self.ssn = TextField(
            api_prediction.get("ssn", {}),
            page_id=page_n,
        )
        self.tax_classification = TextField(
            api_prediction.get("tax_classification", {}),
            page_id=page_n,
        )
        self.tax_classification_llc = TextField(
            api_prediction.get("tax_classification_llc", {}),
            page_id=page_n,
        )
        self.tax_classification_other_details = TextField(
            api_prediction.get("tax_classification_other_details", {}),
            page_id=page_n,
        )
        self.w9_revision_date = TextField(
            api_prediction.get("w9_revision_date", {}),
            page_id=page_n,
        )

    def __str__(self) -> str:
        return clean_out_string(
            "US W9 V1 Prediction\n"
            "======================\n"
            f":Filename: {self.filename or ''}\n"
            f":Name: {self.name}\n"
            f":SSN: {self.ssn}\n"
            f":Address: {self.address}\n"
            f":City State Zip: {self.city_state_zip}\n"
            f":Business Name: {self.business_name}\n"
            f":EIN: {self.ein}\n"
            f":Tax Classification: {self.tax_classification}\n"
            f":Tax Classification Other Details: {self.tax_classification_other_details}\n"
            f":W9 Revision Date: {self.w9_revision_date}\n"
            f":Signature Position: {self.signature_position}\n"
            f":Signature Date Position: {self.signature_date_position}\n"
            f":Tax Classification LLC: {self.tax_classification_llc}\n"
        )


TypeW9V1 = TypeVar(
    "TypeW9V1",
    bound=W9V1,
)
