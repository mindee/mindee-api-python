from typing import Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.date import DateField
from mindee.parsing.standard.text import StringField


class DriverLicenseV1Document(Prediction):
    """Driver License API version 1.0 document data."""

    category: StringField
    """The category or class of the driver license."""
    country_code: StringField
    """The alpha-3 ISO 3166 code of the country where the driver license was issued."""
    date_of_birth: DateField
    """The date of birth of the driver license holder."""
    dd_number: StringField
    """The DD number of the driver license."""
    expiry_date: DateField
    """The expiry date of the driver license."""
    first_name: StringField
    """The first name of the driver license holder."""
    id: StringField
    """The unique identifier of the driver license."""
    issued_date: DateField
    """The date when the driver license was issued."""
    issuing_authority: StringField
    """The authority that issued the driver license."""
    last_name: StringField
    """The last name of the driver license holder."""
    mrz: StringField
    """The Machine Readable Zone (MRZ) of the driver license."""
    place_of_birth: StringField
    """The place of birth of the driver license holder."""
    state: StringField
    """Second part of the ISO 3166-2 code, consisting of two letters indicating the US State."""

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
        self.dd_number = StringField(
            raw_prediction["dd_number"],
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
        self.id = StringField(
            raw_prediction["id"],
            page_id=page_id,
        )
        self.issued_date = DateField(
            raw_prediction["issued_date"],
            page_id=page_id,
        )
        self.issuing_authority = StringField(
            raw_prediction["issuing_authority"],
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
        self.state = StringField(
            raw_prediction["state"],
            page_id=page_id,
        )

    def __str__(self) -> str:
        out_str: str = f":Country Code: {self.country_code}\n"
        out_str += f":State: {self.state}\n"
        out_str += f":ID: {self.id}\n"
        out_str += f":Category: {self.category}\n"
        out_str += f":Last Name: {self.last_name}\n"
        out_str += f":First Name: {self.first_name}\n"
        out_str += f":Date of Birth: {self.date_of_birth}\n"
        out_str += f":Place of Birth: {self.place_of_birth}\n"
        out_str += f":Expiry Date: {self.expiry_date}\n"
        out_str += f":Issued Date: {self.issued_date}\n"
        out_str += f":Issuing Authority: {self.issuing_authority}\n"
        out_str += f":MRZ: {self.mrz}\n"
        out_str += f":DD Number: {self.dd_number}\n"
        return clean_out_string(out_str)
