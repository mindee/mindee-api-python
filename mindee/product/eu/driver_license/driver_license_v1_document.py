from typing import Optional

from mindee.parsing.common import Prediction, StringDict, clean_out_string
from mindee.parsing.standard import DateField, StringField


class DriverLicenseV1Document(Prediction):
    """Driver License API version 1.0 document data."""

    address: StringField
    """EU driver license holders address"""
    category: StringField
    """EU driver license holders categories"""
    country_code: StringField
    """Country code extracted as a string."""
    date_of_birth: DateField
    """The date of birth of the document holder"""
    document_id: StringField
    """ID number of the Document."""
    expiry_date: DateField
    """Date the document expires"""
    first_name: StringField
    """First name(s) of the driver license holder"""
    issue_authority: StringField
    """Authority that issued the document"""
    issue_date: DateField
    """Date the document was issued"""
    last_name: StringField
    """Last name of the driver license holder."""
    mrz: StringField
    """Machine-readable license number"""
    place_of_birth: StringField
    """Place where the driver license holder was born"""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Driver License document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction, page_id)
        self.address = StringField(
            raw_prediction["address"],
            page_id=page_id,
        )
        self.category = StringField(
            raw_prediction["category"],
            page_id=page_id,
        )
        self.country_code = StringField(
            raw_prediction["country_code"],
            page_id=page_id,
        )
        self.date_of_birth = DateField(
            raw_prediction["date_of_birth"],
            page_id=page_id,
        )
        self.document_id = StringField(
            raw_prediction["document_id"],
            page_id=page_id,
        )
        self.expiry_date = DateField(
            raw_prediction["expiry_date"],
            page_id=page_id,
        )
        self.first_name = StringField(
            raw_prediction["first_name"],
            page_id=page_id,
        )
        self.issue_authority = StringField(
            raw_prediction["issue_authority"],
            page_id=page_id,
        )
        self.issue_date = DateField(
            raw_prediction["issue_date"],
            page_id=page_id,
        )
        self.last_name = StringField(
            raw_prediction["last_name"],
            page_id=page_id,
        )
        self.mrz = StringField(
            raw_prediction["mrz"],
            page_id=page_id,
        )
        self.place_of_birth = StringField(
            raw_prediction["place_of_birth"],
            page_id=page_id,
        )

    def __str__(self) -> str:
        out_str: str = f":Country Code: {self.country_code}\n"
        out_str += f":Document ID: {self.document_id}\n"
        out_str += f":Driver License Category: {self.category}\n"
        out_str += f":Last Name: {self.last_name}\n"
        out_str += f":First Name: {self.first_name}\n"
        out_str += f":Date Of Birth: {self.date_of_birth}\n"
        out_str += f":Place Of Birth: {self.place_of_birth}\n"
        out_str += f":Expiry Date: {self.expiry_date}\n"
        out_str += f":Issue Date: {self.issue_date}\n"
        out_str += f":Issue Authority: {self.issue_authority}\n"
        out_str += f":MRZ: {self.mrz}\n"
        out_str += f":Address: {self.address}\n"
        return clean_out_string(out_str)
