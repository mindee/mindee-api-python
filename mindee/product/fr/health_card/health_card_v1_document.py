from typing import List, Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.date import DateField
from mindee.parsing.standard.text import StringField


class HealthCardV1Document(Prediction):
    """Health Card API version 1.0 document data."""

    given_names: List[StringField]
    """The given names of the card holder."""
    issuance_date: DateField
    """The date when the carte vitale document was issued."""
    social_security: StringField
    """The social security number of the card holder."""
    surname: StringField
    """The surname of the card holder."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Health Card document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction, page_id)
        self.given_names = [
            StringField(prediction, page_id=page_id)
            for prediction in raw_prediction["given_names"]
        ]
        self.issuance_date = DateField(
            raw_prediction["issuance_date"],
            page_id=page_id,
        )
        self.social_security = StringField(
            raw_prediction["social_security"],
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
        out_str: str = f":Given Name(s): {given_names}\n"
        out_str += f":Surname: {self.surname}\n"
        out_str += f":Social Security Number: {self.social_security}\n"
        out_str += f":Issuance Date: {self.issuance_date}\n"
        return clean_out_string(out_str)
