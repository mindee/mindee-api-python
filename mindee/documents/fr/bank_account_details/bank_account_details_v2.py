from typing import Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.text import TextField

from .bank_account_details_v2_bban import BankAccountDetailsV2Bban


class BankAccountDetailsV2(Document):
    """Bank Account Details v2 prediction results."""

    account_holders_names: TextField
    """Full extraction of the account holders names."""
    bban: BankAccountDetailsV2Bban
    """Full extraction of BBAN, including: branch code, bank code, account and key."""
    iban: TextField
    """Full extraction of the IBAN number."""
    swift_code: TextField
    """Full extraction of the SWIFT code."""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        """
        Bank Account Details v2 prediction results.

        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type="bank_account_details",
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
        self.account_holders_names = TextField(
            api_prediction["account_holders_names"],
            page_id=page_n,
        )
        self.bban = BankAccountDetailsV2Bban(
            api_prediction["bban"],
            page_id=page_n,
        )
        self.iban = TextField(
            api_prediction["iban"],
            page_id=page_n,
        )
        self.swift_code = TextField(
            api_prediction["swift_code"],
            page_id=page_n,
        )

    def __str__(self) -> str:
        return clean_out_string(
            "FR Bank Account Details V2 Prediction\n"
            "=====================================\n"
            f":Filename: {self.filename or ''}\n"
            f":Account Holder's Names: {self.account_holders_names}\n"
            f":Basic Bank Account Number:\n{self.bban.to_field_list()}\n"
            f":IBAN: {self.iban}\n"
            f":SWIFT Code: {self.swift_code}\n"
        )


TypeBankAccountDetailsV2 = TypeVar(
    "TypeBankAccountDetailsV2",
    bound=BankAccountDetailsV2,
)
