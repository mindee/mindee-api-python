from typing import Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.text import TextField


class BankAccountDetailsV1(Document):
    """Bank Account Details v1 prediction results."""

    account_holder_name: TextField
    """The name of the account holder as seen on the document."""
    iban: TextField
    """The International Bank Account Number (IBAN)."""
    swift: TextField
    """The bank's SWIFT Business Identifier Code (BIC)."""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        """
        Bank Account Details v1 prediction results.

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
        self.account_holder_name = TextField(
            api_prediction["account_holder_name"],
            page_id=page_n,
        )
        self.iban = TextField(
            api_prediction["iban"],
            page_id=page_n,
        )
        self.swift = TextField(
            api_prediction["swift"],
            page_id=page_n,
        )

    def __str__(self) -> str:
        return clean_out_string(
            "FR Bank Account Details V1 Prediction\n"
            "=====================================\n"
            f":Filename: {self.filename or ''}\n"
            f":IBAN: {self.iban}\n"
            f":Account Holder's Name: {self.account_holder_name}\n"
            f":SWIFT Code: {self.swift}\n"
        )


TypeBankAccountDetailsV1 = TypeVar(
    "TypeBankAccountDetailsV1",
    bound=BankAccountDetailsV1,
)
