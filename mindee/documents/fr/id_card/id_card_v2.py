from typing import List, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.classification import ClassificationField
from mindee.fields.date import DateField
from mindee.fields.text import TextField


class IdCardV2(Document):
    """Carte Nationale d'Identité v2 prediction results."""

    alternate_name: TextField
    """The alternate name of the card holder."""
    authority: TextField
    """The name of the issuing authority."""
    birth_date: DateField
    """The date of birth of the card holder."""
    birth_place: TextField
    """The place of birth of the card holder."""
    card_access_number: TextField
    """The card access number (CAN)."""
    document_number: TextField
    """The document number."""
    document_side: ClassificationField
    """The sides of the document which are visible."""
    document_type: ClassificationField
    """The document type or format."""
    expiry_date: DateField
    """The expiry date of the identification card."""
    gender: TextField
    """The gender of the card holder."""
    given_names: List[TextField]
    """The given name(s) of the card holder."""
    issue_date: DateField
    """The date of issue of the identification card."""
    mrz1: TextField
    """The Machine Readable Zone, first line."""
    mrz2: TextField
    """The Machine Readable Zone, second line."""
    mrz3: TextField
    """The Machine Readable Zone, third line."""
    nationality: TextField
    """The nationality of the card holder."""
    surname: TextField
    """The surname of the card holder."""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        """
        Carte Nationale d'Identité v2 prediction results.

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
        self.alternate_name = TextField(
            api_prediction["alternate_name"],
            page_id=page_n,
        )
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
        self.card_access_number = TextField(
            api_prediction["card_access_number"],
            page_id=page_n,
        )
        self.document_number = TextField(
            api_prediction["document_number"],
            page_id=page_n,
        )
        self.document_side = ClassificationField(
            api_prediction.get("document_side", {}),
            page_id=page_n,
        )
        self.document_type = ClassificationField(
            api_prediction.get("document_type", {}),
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
        self.issue_date = DateField(
            api_prediction["issue_date"],
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
        self.mrz3 = TextField(
            api_prediction["mrz3"],
            page_id=page_n,
        )
        self.nationality = TextField(
            api_prediction["nationality"],
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
            "FR Carte Nationale d'Identité V2 Prediction\n"
            "===========================================\n"
            f":Filename: {self.filename or ''}\n"
            f":Document Type: {self.document_type}\n"
            f":Document Sides: {self.document_side}\n"
            f":Nationality: {self.nationality}\n"
            f":Card Access Number: {self.card_access_number}\n"
            f":Document Number: {self.document_number}\n"
            f":Given Name(s): {given_names}\n"
            f":Surname: {self.surname}\n"
            f":Alternate Name: {self.alternate_name}\n"
            f":Date of Birth: {self.birth_date}\n"
            f":Place of Birth: {self.birth_place}\n"
            f":Gender: {self.gender}\n"
            f":Expiry Date: {self.expiry_date}\n"
            f":Mrz Line 1: {self.mrz1}\n"
            f":Mrz Line 2: {self.mrz2}\n"
            f":Mrz Line 3: {self.mrz3}\n"
            f":Date of Issue: {self.issue_date}\n"
            f":Issuing Authority: {self.authority}\n"
        )


TypeIdCardV2 = TypeVar(
    "TypeIdCardV2",
    bound=IdCardV2,
)
