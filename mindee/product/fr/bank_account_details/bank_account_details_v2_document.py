from typing import Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.text import StringField
from mindee.product.fr.bank_account_details.bank_account_details_v2_bban import (
    BankAccountDetailsV2Bban,
)


class BankAccountDetailsV2Document(Prediction):
    """Bank Account Details API version 2.0 document data."""

    account_holders_names: StringField
    """Full extraction of the account holders names."""
    bban: BankAccountDetailsV2Bban
    """Full extraction of BBAN, including: branch code, bank code, account and key."""
    iban: StringField
    """Full extraction of the IBAN number."""
    swift_code: StringField
    """Full extraction of the SWIFT code."""

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
        self.account_holders_names = StringField(
            raw_prediction["account_holders_names"],
            page_id=page_id,
        )
        self.bban = BankAccountDetailsV2Bban(
            raw_prediction["bban"],
            page_id=page_id,
        )
        self.iban = StringField(
            raw_prediction["iban"],
            page_id=page_id,
        )
        self.swift_code = StringField(
            raw_prediction["swift_code"],
            page_id=page_id,
        )

    def __str__(self) -> str:
        out_str: str = f":Account Holder's Names: {self.account_holders_names}\n"
        out_str += f":Basic Bank Account Number:\n{self.bban.to_field_list()}\n"
        out_str += f":IBAN: {self.iban}\n"
        out_str += f":SWIFT Code: {self.swift_code}\n"
        return clean_out_string(out_str)
