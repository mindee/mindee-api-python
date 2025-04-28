from typing import List, Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.classification import ClassificationField
from mindee.parsing.standard.date import DateField
from mindee.parsing.standard.text import StringField


class InternationalIdV2Document(Prediction):
    """International ID API version 2.2 document data."""

    address: StringField
    """The physical address of the document holder."""
    birth_date: DateField
    """The date of birth of the document holder."""
    birth_place: StringField
    """The place of birth of the document holder."""
    country_of_issue: StringField
    """The country where the document was issued."""
    document_number: StringField
    """The unique identifier assigned to the document."""
    document_type: ClassificationField
    """The type of personal identification document."""
    expiry_date: DateField
    """The date when the document becomes invalid."""
    given_names: List[StringField]
    """The list of the document holder's given names."""
    issue_date: DateField
    """The date when the document was issued."""
    mrz_line1: StringField
    """The Machine Readable Zone, first line."""
    mrz_line2: StringField
    """The Machine Readable Zone, second line."""
    mrz_line3: StringField
    """The Machine Readable Zone, third line."""
    nationality: StringField
    """The country of citizenship of the document holder."""
    personal_number: StringField
    """The unique identifier assigned to the document holder."""
    sex: StringField
    """The biological sex of the document holder."""
    state_of_issue: StringField
    """The state or territory where the document was issued."""
    surnames: List[StringField]
    """The list of the document holder's family names."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        International ID document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction, page_id)
        self.address = StringField(
            raw_prediction["address"],
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
        self.country_of_issue = StringField(
            raw_prediction["country_of_issue"],
            page_id=page_id,
        )
        self.document_number = StringField(
            raw_prediction["document_number"],
            page_id=page_id,
        )
        self.document_type = ClassificationField(
            raw_prediction["document_type"],
            page_id=page_id,
        )
        self.expiry_date = DateField(
            raw_prediction["expiry_date"],
            page_id=page_id,
        )
        self.given_names = [
            StringField(prediction, page_id=page_id)
            for prediction in raw_prediction["given_names"]
        ]
        self.issue_date = DateField(
            raw_prediction["issue_date"],
            page_id=page_id,
        )
        self.mrz_line1 = StringField(
            raw_prediction["mrz_line1"],
            page_id=page_id,
        )
        self.mrz_line2 = StringField(
            raw_prediction["mrz_line2"],
            page_id=page_id,
        )
        self.mrz_line3 = StringField(
            raw_prediction["mrz_line3"],
            page_id=page_id,
        )
        self.nationality = StringField(
            raw_prediction["nationality"],
            page_id=page_id,
        )
        self.personal_number = StringField(
            raw_prediction["personal_number"],
            page_id=page_id,
        )
        self.sex = StringField(
            raw_prediction["sex"],
            page_id=page_id,
        )
        self.state_of_issue = StringField(
            raw_prediction["state_of_issue"],
            page_id=page_id,
        )
        self.surnames = [
            StringField(prediction, page_id=page_id)
            for prediction in raw_prediction["surnames"]
        ]

    def __str__(self) -> str:
        given_names = f"\n { ' ' * 13 }".join(
            [str(item) for item in self.given_names],
        )
        surnames = f"\n { ' ' * 10 }".join(
            [str(item) for item in self.surnames],
        )
        out_str: str = f":Document Type: {self.document_type}\n"
        out_str += f":Document Number: {self.document_number}\n"
        out_str += f":Surnames: {surnames}\n"
        out_str += f":Given Names: {given_names}\n"
        out_str += f":Sex: {self.sex}\n"
        out_str += f":Birth Date: {self.birth_date}\n"
        out_str += f":Birth Place: {self.birth_place}\n"
        out_str += f":Nationality: {self.nationality}\n"
        out_str += f":Personal Number: {self.personal_number}\n"
        out_str += f":Country of Issue: {self.country_of_issue}\n"
        out_str += f":State of Issue: {self.state_of_issue}\n"
        out_str += f":Issue Date: {self.issue_date}\n"
        out_str += f":Expiration Date: {self.expiry_date}\n"
        out_str += f":Address: {self.address}\n"
        out_str += f":MRZ Line 1: {self.mrz_line1}\n"
        out_str += f":MRZ Line 2: {self.mrz_line2}\n"
        out_str += f":MRZ Line 3: {self.mrz_line3}\n"
        return clean_out_string(out_str)
