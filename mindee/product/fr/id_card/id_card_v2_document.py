from typing import List, Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.date import DateField
from mindee.parsing.standard.text import StringField


class IdCardV2Document(Prediction):
    """Carte Nationale d'Identité API version 2.0 document data."""

    alternate_name: StringField
    """The alternate name of the card holder."""
    authority: StringField
    """The name of the issuing authority."""
    birth_date: DateField
    """The date of birth of the card holder."""
    birth_place: StringField
    """The place of birth of the card holder."""
    card_access_number: StringField
    """The card access number (CAN)."""
    document_number: StringField
    """The document number."""
    expiry_date: DateField
    """The expiry date of the identification card."""
    gender: StringField
    """The gender of the card holder."""
    given_names: List[StringField]
    """The given name(s) of the card holder."""
    issue_date: DateField
    """The date of issue of the identification card."""
    mrz1: StringField
    """The Machine Readable Zone, first line."""
    mrz2: StringField
    """The Machine Readable Zone, second line."""
    mrz3: StringField
    """The Machine Readable Zone, third line."""
    nationality: StringField
    """The nationality of the card holder."""
    surname: StringField
    """The surname of the card holder."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Carte Nationale d'Identité document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction, page_id)
        self.alternate_name = StringField(
            raw_prediction["alternate_name"],
            page_id=page_id,
        )
        self.authority = StringField(
            raw_prediction["authority"],
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
        self.card_access_number = StringField(
            raw_prediction["card_access_number"],
            page_id=page_id,
        )
        self.document_number = StringField(
            raw_prediction["document_number"],
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
        self.surname = StringField(
            raw_prediction["surname"],
            page_id=page_id,
        )

    def __str__(self) -> str:
        given_names = f"\n { ' ' * 15 }".join(
            [str(item) for item in self.given_names],
        )
        out_str: str = f":Nationality: {self.nationality}\n"
        out_str += f":Card Access Number: {self.card_access_number}\n"
        out_str += f":Document Number: {self.document_number}\n"
        out_str += f":Given Name(s): {given_names}\n"
        out_str += f":Surname: {self.surname}\n"
        out_str += f":Alternate Name: {self.alternate_name}\n"
        out_str += f":Date of Birth: {self.birth_date}\n"
        out_str += f":Place of Birth: {self.birth_place}\n"
        out_str += f":Gender: {self.gender}\n"
        out_str += f":Expiry Date: {self.expiry_date}\n"
        out_str += f":Mrz Line 1: {self.mrz1}\n"
        out_str += f":Mrz Line 2: {self.mrz2}\n"
        out_str += f":Mrz Line 3: {self.mrz3}\n"
        out_str += f":Date of Issue: {self.issue_date}\n"
        out_str += f":Issuing Authority: {self.authority}\n"
        return clean_out_string(out_str)
