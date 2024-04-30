from typing import Optional

from mindee.parsing.common import Prediction, StringDict, clean_out_string
from mindee.parsing.standard import DateField, StringField


class DriverLicenseV1Document(Prediction):
    """Driver License API version 1.1 document data."""

    address: StringField
    """US driver license holders address"""
    date_of_birth: DateField
    """US driver license holders date of birth"""
    dd_number: StringField
    """Document Discriminator Number of the US Driver License"""
    dl_class: StringField
    """US driver license holders class"""
    driver_license_id: StringField
    """ID number of the US Driver License."""
    endorsements: StringField
    """US driver license holders endorsements"""
    expiry_date: DateField
    """Date on which the documents expires."""
    eye_color: StringField
    """US driver license holders eye colour"""
    first_name: StringField
    """US driver license holders first name(s)"""
    hair_color: StringField
    """US driver license holders hair colour"""
    height: StringField
    """US driver license holders hight"""
    issued_date: DateField
    """Date on which the documents was issued."""
    last_name: StringField
    """US driver license holders last name"""
    restrictions: StringField
    """US driver license holders restrictions"""
    sex: StringField
    """US driver license holders gender"""
    state: StringField
    """US State"""
    weight: StringField
    """US driver license holders weight"""

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
        self.date_of_birth = DateField(
            raw_prediction["date_of_birth"],
            page_id=page_id,
        )
        self.dd_number = StringField(
            raw_prediction["dd_number"],
            page_id=page_id,
        )
        self.dl_class = StringField(
            raw_prediction["dl_class"],
            page_id=page_id,
        )
        self.driver_license_id = StringField(
            raw_prediction["driver_license_id"],
            page_id=page_id,
        )
        self.endorsements = StringField(
            raw_prediction["endorsements"],
            page_id=page_id,
        )
        self.expiry_date = DateField(
            raw_prediction["expiry_date"],
            page_id=page_id,
        )
        self.eye_color = StringField(
            raw_prediction["eye_color"],
            page_id=page_id,
        )
        self.first_name = StringField(
            raw_prediction["first_name"],
            page_id=page_id,
        )
        self.hair_color = StringField(
            raw_prediction["hair_color"],
            page_id=page_id,
        )
        self.height = StringField(
            raw_prediction["height"],
            page_id=page_id,
        )
        self.issued_date = DateField(
            raw_prediction["issued_date"],
            page_id=page_id,
        )
        self.last_name = StringField(
            raw_prediction["last_name"],
            page_id=page_id,
        )
        self.restrictions = StringField(
            raw_prediction["restrictions"],
            page_id=page_id,
        )
        self.sex = StringField(
            raw_prediction["sex"],
            page_id=page_id,
        )
        self.state = StringField(
            raw_prediction["state"],
            page_id=page_id,
        )
        self.weight = StringField(
            raw_prediction["weight"],
            page_id=page_id,
        )

    def __str__(self) -> str:
        out_str: str = f":State: {self.state}\n"
        out_str += f":Driver License ID: {self.driver_license_id}\n"
        out_str += f":Expiry Date: {self.expiry_date}\n"
        out_str += f":Date Of Issue: {self.issued_date}\n"
        out_str += f":Last Name: {self.last_name}\n"
        out_str += f":First Name: {self.first_name}\n"
        out_str += f":Address: {self.address}\n"
        out_str += f":Date Of Birth: {self.date_of_birth}\n"
        out_str += f":Restrictions: {self.restrictions}\n"
        out_str += f":Endorsements: {self.endorsements}\n"
        out_str += f":Driver License Class: {self.dl_class}\n"
        out_str += f":Sex: {self.sex}\n"
        out_str += f":Height: {self.height}\n"
        out_str += f":Weight: {self.weight}\n"
        out_str += f":Hair Color: {self.hair_color}\n"
        out_str += f":Eye Color: {self.eye_color}\n"
        out_str += f":Document Discriminator: {self.dd_number}\n"
        return clean_out_string(out_str)
