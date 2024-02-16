from typing import List, Optional

from mindee.parsing.common import Prediction, StringDict, clean_out_string
from mindee.parsing.standard import ClassificationField, DateField, StringField


class InternationalIdV1Document(Prediction):
    """Document data for International ID, API version 1."""

    address: StringField
    """The physical location of the document holder's residence."""
    birth_date: DateField
    """The date of birth of the document holder."""
    birth_place: StringField
    """The location where the document holder was born."""
    country_of_issue: StringField
    """The country that issued the identification document."""
    document_number: StringField
    """The unique identifier assigned to the identification document."""
    document_type: ClassificationField
    """The type of identification document being used."""
    expiry_date: DateField
    """The date when the document will no longer be valid for use."""
    given_names: List[StringField]
    """The first names or given names of the document holder."""
    issue_date: DateField
    """The date when the document was issued."""
    mrz1: StringField
    """First line of information in a standardized format for easy machine reading and processing."""
    mrz2: StringField
    """Second line of information in a standardized format for easy machine reading and processing."""
    mrz3: StringField
    """Third line of information in a standardized format for easy machine reading and processing."""
    nationality: StringField
    """Indicates the country of citizenship or nationality of the document holder."""
    sex: StringField
    """The document holder's biological sex, such as male or female."""
    surnames: List[StringField]
    """The surnames of the document holder."""

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
        self.mrz1 = StringField(
            raw_prediction["mrz1"],
            page_id=page_id,
        )
        self.mrz2 = StringField(
            raw_prediction["mrz2"],
            page_id=page_id,
        )
        self.mrz3 = StringField(
            raw_prediction["mrz3"],
            page_id=page_id,
        )
        self.nationality = StringField(
            raw_prediction["nationality"],
            page_id=page_id,
        )
        self.sex = StringField(
            raw_prediction["sex"],
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
        out_str += f":Country of Issue: {self.country_of_issue}\n"
        out_str += f":Surnames: {surnames}\n"
        out_str += f":Given Names: {given_names}\n"
        out_str += f":Gender: {self.sex}\n"
        out_str += f":Birth date: {self.birth_date}\n"
        out_str += f":Birth Place: {self.birth_place}\n"
        out_str += f":Nationality: {self.nationality}\n"
        out_str += f":Issue Date: {self.issue_date}\n"
        out_str += f":Expiry Date: {self.expiry_date}\n"
        out_str += f":Address: {self.address}\n"
        out_str += f":Machine Readable Zone Line 1: {self.mrz1}\n"
        out_str += f":Machine Readable Zone Line 2: {self.mrz2}\n"
        out_str += f":Machine Readable Zone Line 3: {self.mrz3}\n"
        return clean_out_string(out_str)
