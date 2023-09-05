from typing import List, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.classification import ClassificationField
from mindee.fields.date import DateField
from mindee.fields.text import TextField


class IdCardV1(Document):
    """Carte Nationale d'Identité v1 prediction results."""

    authority: TextField
    """The name of the issuing authority."""
    birth_date: DateField
    """The date of birth of the card holder."""
    birth_place: TextField
    """The place of birth of the card holder."""
    document_side: ClassificationField
    """The side of the document which is visible."""
    expiry_date: DateField
    """The expiry date of the identification card."""
    gender: TextField
    """The gender of the card holder."""
    given_names: List[TextField]
    """The given name(s) of the card holder."""
    id_number: TextField
    """The identification card number."""
    mrz1: TextField
    """Machine Readable Zone, first line"""
    mrz2: TextField
    """Machine Readable Zone, second line"""
    surname: TextField
    """The surname of the card holder."""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        """
        Carte Nationale d'Identité v1 prediction results.

        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type="id_card",
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
        self.authority = TextField(
            api_prediction["authority"],
            page_id=page_n,
        )
        self.birth_date = DateField(
            api_prediction["birth_date"],
            page_id=page_n,
        )
        self.birth_place = TextField(
            api_prediction["birth_place"],
            page_id=page_n,
        )
        self.document_side = ClassificationField(
            api_prediction.get("document_side", {}),
            page_id=page_n,
        )
        self.expiry_date = DateField(
            api_prediction["expiry_date"],
            page_id=page_n,
        )
        self.gender = TextField(
            api_prediction["gender"],
            page_id=page_n,
        )
        self.given_names = [
            TextField(prediction, page_id=page_n)
            for prediction in api_prediction["given_names"]
        ]
        self.id_number = TextField(
            api_prediction["id_number"],
            page_id=page_n,
        )
        self.mrz1 = TextField(
            api_prediction["mrz1"],
            page_id=page_n,
        )
        self.mrz2 = TextField(
            api_prediction["mrz2"],
            page_id=page_n,
        )
        self.surname = TextField(
            api_prediction["surname"],
            page_id=page_n,
        )

    def __str__(self) -> str:
        given_names = f"\n { ' ' * 15 }".join(
            [str(item) for item in self.given_names],
        )
        return clean_out_string(
            "FR Carte Nationale d'Identité V1 Prediction\n"
            "===========================================\n"
            f":Filename: {self.filename or ''}\n"
            f":Document Side: {self.document_side}\n"
            f":Identity Number: {self.id_number}\n"
            f":Given Name(s): {given_names}\n"
            f":Surname: {self.surname}\n"
            f":Date of Birth: {self.birth_date}\n"
            f":Place of Birth: {self.birth_place}\n"
            f":Expiry Date: {self.expiry_date}\n"
            f":Issuing Authority: {self.authority}\n"
            f":Gender: {self.gender}\n"
            f":MRZ Line 1: {self.mrz1}\n"
            f":MRZ Line 2: {self.mrz2}\n"
        )


TypeIdCardV1 = TypeVar(
    "TypeIdCardV1",
    bound=IdCardV1,
)
