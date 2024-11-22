from typing import Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.text import StringField


class BankAccountDetailsV1Document(Prediction):
    """Bank Account Details API version 1.0 document data."""

    account_holder_name: StringField
    """The name of the account holder as seen on the document."""
    iban: StringField
    """The International Bank Account Number (IBAN)."""
    swift: StringField
    """The bank's SWIFT Business Identifier Code (BIC)."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Bank Account Details document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction, page_id)
        self.account_holder_name = StringField(
            raw_prediction["account_holder_name"],
            page_id=page_id,
        )
        self.iban = StringField(
            raw_prediction["iban"],
            page_id=page_id,
        )
        self.swift = StringField(
            raw_prediction["swift"],
            page_id=page_id,
        )

    def __str__(self) -> str:
        out_str: str = f":IBAN: {self.iban}\n"
        out_str += f":Account Holder's Name: {self.account_holder_name}\n"
        out_str += f":SWIFT Code: {self.swift}\n"
        return clean_out_string(out_str)
