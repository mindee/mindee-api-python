from typing import List, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.amount import AmountField
from mindee.fields.date import DateField
from mindee.fields.position import PositionField
from mindee.fields.text import TextField


class BankCheckV1(Document):
    """Bank Check v1 prediction results."""

    account_number: TextField
    """The check payer's account number."""
    amount: AmountField
    """The amount of the check."""
    check_number: TextField
    """The issuer's check number."""
    check_position: PositionField
    """The position of the check on the document."""
    date: DateField
    """The date the check was issued."""
    payees: List[TextField]
    """List of the check's payees (recipients)."""
    routing_number: TextField
    """The check issuer's routing number."""
    signatures_positions: List[PositionField]
    """List of signature positions"""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        """
        Bank Check v1 prediction results.

        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type="bank_check",
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
        self.account_number = TextField(
            api_prediction["account_number"],
            page_id=page_n,
        )
        self.amount = AmountField(
            api_prediction["amount"],
            page_id=page_n,
        )
        self.check_number = TextField(
            api_prediction["check_number"],
            page_id=page_n,
        )
        self.check_position = PositionField(
            api_prediction.get("check_position", {}),
            page_id=page_n,
        )
        self.date = DateField(
            api_prediction["date"],
            page_id=page_n,
        )
        self.payees = [
            TextField(prediction, page_id=page_n)
            for prediction in api_prediction["payees"]
        ]
        self.routing_number = TextField(
            api_prediction["routing_number"],
            page_id=page_n,
        )
        self.signatures_positions = [
            PositionField(prediction, page_id=page_n)
            for prediction in api_prediction["signatures_positions"]
        ]

    def __str__(self) -> str:
        payees = f"\n { ' ' * 8 }".join(
            [str(item) for item in self.payees],
        )
        signatures_positions = f"\n { ' ' * 21 }".join(
            [str(item) for item in self.signatures_positions],
        )
        return clean_out_string(
            "US Bank Check V1 Prediction\n"
            "===========================\n"
            f":Filename: {self.filename or ''}\n"
            f":Check Position: {self.check_position}\n"
            f":Signature Positions: {signatures_positions}\n"
            f":Check Issue Date: {self.date}\n"
            f":Amount: {self.amount}\n"
            f":Payees: {payees}\n"
            f":Routing Number: {self.routing_number}\n"
            f":Account Number: {self.account_number}\n"
            f":Check Number: {self.check_number}\n"
        )


TypeBankCheckV1 = TypeVar(
    "TypeBankCheckV1",
    bound=BankCheckV1,
)
