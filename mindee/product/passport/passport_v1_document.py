from typing import List, Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.date import DateField
from mindee.parsing.standard.text import StringField


class PassportV1Document(Prediction):
    """Passport API version 1.1 document data."""

    birth_date: DateField
    """The date of birth of the passport holder."""
    birth_place: StringField
    """The place of birth of the passport holder."""
    country: StringField
    """The country's 3 letter code (ISO 3166-1 alpha-3)."""
    expiry_date: DateField
    """The expiry date of the passport."""
    gender: StringField
    """The gender of the passport holder."""
    given_names: List[StringField]
    """The given name(s) of the passport holder."""
    id_number: StringField
    """The passport's identification number."""
    issuance_date: DateField
    """The date the passport was issued."""
    mrz1: StringField
    """Machine Readable Zone, first line"""
    mrz2: StringField
    """Machine Readable Zone, second line"""
    surname: StringField
    """The surname of the passport holder."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Passport document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction, page_id)
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
        self.gender = StringField(
            raw_prediction["gender"],
            page_id=page_id,
        )
        self.given_names = [
            StringField(prediction, page_id=page_id)
            for prediction in raw_prediction["given_names"]
        ]
        self.id_number = StringField(
            raw_prediction["id_number"],
            page_id=page_id,
        )
        self.issuance_date = DateField(
            raw_prediction["issuance_date"],
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
        self.surname = StringField(
            raw_prediction["surname"],
            page_id=page_id,
        )

    def __str__(self) -> str:
        given_names = f"\n { ' ' * 15 }".join(
            [str(item) for item in self.given_names],
        )
        out_str: str = f":Country Code: {self.country}\n"
        out_str += f":ID Number: {self.id_number}\n"
        out_str += f":Given Name(s): {given_names}\n"
        out_str += f":Surname: {self.surname}\n"
        out_str += f":Date of Birth: {self.birth_date}\n"
        out_str += f":Place of Birth: {self.birth_place}\n"
        out_str += f":Gender: {self.gender}\n"
        out_str += f":Date of Issue: {self.issuance_date}\n"
        out_str += f":Expiry Date: {self.expiry_date}\n"
        out_str += f":MRZ Line 1: {self.mrz1}\n"
        out_str += f":MRZ Line 2: {self.mrz2}\n"
        return clean_out_string(out_str)
