from typing import List, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.date import DateField
from mindee.fields.text import TextField


class CarteVitaleV1(Document):
    """A Carte Vitale prediction."""

    given_names: List[TextField]
    """The given name(s) of the card holder."""
    surname: TextField
    """The surname of the card holder."""
    social_security: TextField
    """The Social Security Number (Numéro de Sécurité Sociale) of the card holder"""
    issuance_date: DateField
    """The date the card was issued."""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
        document_type="carte_vitale",
    ):
        """
         document.

        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type=document_type,
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
            TextField(prediction, page_n=page_n)
            for prediction in api_prediction["given_names"]
        ]
        self.surname = TextField(
            api_prediction["surname"],
            page_n=page_n,
        )
        self.social_security = TextField(
            api_prediction["social_security"],
            page_n=page_n,
        )
        self.issuance_date = DateField(
            api_prediction["issuance_date"],
            page_n=page_n,
        )

    def __str__(self) -> str:
        return clean_out_string(
            "----- Carte Vitale V1 -----\n"
            f"Given Name(s): {self.given_names}"
            f"Surname: {self.surname}"
            f"Social Security Number: {self.social_security}"
            f"Issuance Date: {self.issuance_date}"
            "----------------------"
        )


TypeCarteVitaleV1 = TypeVar("TypeCarteVitaleV1", bound=CarteVitaleV1)
