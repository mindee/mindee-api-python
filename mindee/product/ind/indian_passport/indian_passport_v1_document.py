from typing import Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.classification import ClassificationField
from mindee.parsing.standard.date import DateField
from mindee.parsing.standard.text import StringField


class IndianPassportV1Document(Prediction):
    """Passport - India API version 1.2 document data."""

    address1: StringField
    """The first line of the address of the passport holder."""
    address2: StringField
    """The second line of the address of the passport holder."""
    address3: StringField
    """The third line of the address of the passport holder."""
    birth_date: DateField
    """The birth date of the passport holder, ISO format: YYYY-MM-DD."""
    birth_place: StringField
    """The birth place of the passport holder."""
    country: StringField
    """ISO 3166-1 alpha-3 country code (3 letters format)."""
    expiry_date: DateField
    """The date when the passport will expire, ISO format: YYYY-MM-DD."""
    file_number: StringField
    """The file number of the passport document."""
    gender: ClassificationField
    """The gender of the passport holder."""
    given_names: StringField
    """The given names of the passport holder."""
    id_number: StringField
    """The identification number of the passport document."""
    issuance_date: DateField
    """The date when the passport was issued, ISO format: YYYY-MM-DD."""
    issuance_place: StringField
    """The place where the passport was issued."""
    legal_guardian: StringField
    """The name of the legal guardian of the passport holder (if applicable)."""
    mrz1: StringField
    """The first line of the machine-readable zone (MRZ) of the passport document."""
    mrz2: StringField
    """The second line of the machine-readable zone (MRZ) of the passport document."""
    name_of_mother: StringField
    """The name of the mother of the passport holder."""
    name_of_spouse: StringField
    """The name of the spouse of the passport holder (if applicable)."""
    old_passport_date_of_issue: DateField
    """The date of issue of the old passport (if applicable), ISO format: YYYY-MM-DD."""
    old_passport_number: StringField
    """The number of the old passport (if applicable)."""
    old_passport_place_of_issue: StringField
    """The place of issue of the old passport (if applicable)."""
    page_number: ClassificationField
    """The page number of the passport document."""
    surname: StringField
    """The surname of the passport holder."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Passport - India document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction, page_id)
        self.address1 = StringField(
            raw_prediction["address1"],
            page_id=page_id,
        )
        self.address2 = StringField(
            raw_prediction["address2"],
            page_id=page_id,
        )
        self.address3 = StringField(
            raw_prediction["address3"],
            page_id=page_id,
        )
        self.birth_date = DateField(
            raw_prediction["birth_date"],
            page_id=page_id,
        )
        self.birth_place = StringField(
            raw_prediction["birth_place"],
            page_id=page_id,
        )
        self.country = StringField(
            raw_prediction["country"],
            page_id=page_id,
        )
        self.expiry_date = DateField(
            raw_prediction["expiry_date"],
            page_id=page_id,
        )
        self.file_number = StringField(
            raw_prediction["file_number"],
            page_id=page_id,
        )
        self.gender = ClassificationField(
            raw_prediction["gender"],
            page_id=page_id,
        )
        self.given_names = StringField(
            raw_prediction["given_names"],
            page_id=page_id,
        )
        self.id_number = StringField(
            raw_prediction["id_number"],
            page_id=page_id,
        )
        self.issuance_date = DateField(
            raw_prediction["issuance_date"],
            page_id=page_id,
        )
        self.issuance_place = StringField(
            raw_prediction["issuance_place"],
            page_id=page_id,
        )
        self.legal_guardian = StringField(
            raw_prediction["legal_guardian"],
            page_id=page_id,
        )
        self.mrz1 = StringField(
            raw_prediction["mrz1"],
            page_id=page_id,
        )
        self.mrz2 = StringField(
            raw_prediction["mrz2"],
            page_id=page_id,
        )
        self.name_of_mother = StringField(
            raw_prediction["name_of_mother"],
            page_id=page_id,
        )
        self.name_of_spouse = StringField(
            raw_prediction["name_of_spouse"],
            page_id=page_id,
        )
        self.old_passport_date_of_issue = DateField(
            raw_prediction["old_passport_date_of_issue"],
            page_id=page_id,
        )
        self.old_passport_number = StringField(
            raw_prediction["old_passport_number"],
            page_id=page_id,
        )
        self.old_passport_place_of_issue = StringField(
            raw_prediction["old_passport_place_of_issue"],
            page_id=page_id,
        )
        self.page_number = ClassificationField(
            raw_prediction["page_number"],
            page_id=page_id,
        )
        self.surname = StringField(
            raw_prediction["surname"],
            page_id=page_id,
        )

    def __str__(self) -> str:
        out_str: str = f":Page Number: {self.page_number}\n"
        out_str += f":Country: {self.country}\n"
        out_str += f":ID Number: {self.id_number}\n"
        out_str += f":Given Names: {self.given_names}\n"
        out_str += f":Surname: {self.surname}\n"
        out_str += f":Birth Date: {self.birth_date}\n"
        out_str += f":Birth Place: {self.birth_place}\n"
        out_str += f":Issuance Place: {self.issuance_place}\n"
        out_str += f":Gender: {self.gender}\n"
        out_str += f":Issuance Date: {self.issuance_date}\n"
        out_str += f":Expiry Date: {self.expiry_date}\n"
        out_str += f":MRZ Line 1: {self.mrz1}\n"
        out_str += f":MRZ Line 2: {self.mrz2}\n"
        out_str += f":Legal Guardian: {self.legal_guardian}\n"
        out_str += f":Name of Spouse: {self.name_of_spouse}\n"
        out_str += f":Name of Mother: {self.name_of_mother}\n"
        out_str += f":Old Passport Date of Issue: {self.old_passport_date_of_issue}\n"
        out_str += f":Old Passport Number: {self.old_passport_number}\n"
        out_str += f":Old Passport Place of Issue: {self.old_passport_place_of_issue}\n"
        out_str += f":Address Line 1: {self.address1}\n"
        out_str += f":Address Line 2: {self.address2}\n"
        out_str += f":Address Line 3: {self.address3}\n"
        out_str += f":File Number: {self.file_number}\n"
        return clean_out_string(out_str)
