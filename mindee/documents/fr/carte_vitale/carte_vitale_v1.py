from typing import List, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.date import DateField
from mindee.fields.text import TextField


class CarteVitaleV1(Document):
    """Carte Vitale v1 prediction results."""

    given_names: List[TextField]
    """The given name(s) of the card holder."""
    issuance_date: DateField
    """The date the card was issued."""
    social_security: TextField
    """The Social Security Number (Numéro de Sécurité Sociale) of the card holder"""
    surname: TextField
    """The surname of the card holder."""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        """
        Carte Vitale v1 prediction results.

        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type="carte_vitale",
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
        self.given_names = [
            TextField(prediction, page_id=page_n)
            for prediction in api_prediction["given_names"]
        ]
        self.issuance_date = DateField(
            api_prediction["issuance_date"],
            page_id=page_n,
        )
        self.social_security = TextField(
            api_prediction["social_security"],
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
            "FR Carte Vitale V1 Prediction\n"
            "=============================\n"
            f":Filename: {self.filename or ''}\n"
            f":Given Name(s): {given_names}\n"
            f":Surname: {self.surname}\n"
            f":Social Security Number: {self.social_security}\n"
            f":Issuance Date: {self.issuance_date}\n"
        )


TypeCarteVitaleV1 = TypeVar(
    "TypeCarteVitaleV1",
    bound=CarteVitaleV1,
)
