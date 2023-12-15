from typing import List, Optional

from mindee.parsing.common import Prediction, StringDict, clean_out_string
from mindee.parsing.standard import AmountField, DateField, StringField


class BankCheckV1Document(Prediction):
    """Document data for Bank Check, API version 1."""

    account_number: StringField
    """The check payer's account number."""
    amount: AmountField
    """The amount of the check."""
    check_number: StringField
    """The issuer's check number."""
    date: DateField
    """The date the check was issued."""
    payees: List[StringField]
    """List of the check's payees (recipients)."""
    routing_number: StringField
    """The check issuer's routing number."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Bank Check document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        self.account_number = StringField(
            raw_prediction["account_number"],
            page_id=page_id,
        )
        self.amount = AmountField(
            raw_prediction["amount"],
            page_id=page_id,
        )
        self.check_number = StringField(
            raw_prediction["check_number"],
            page_id=page_id,
        )
        self.date = DateField(
            raw_prediction["date"],
            page_id=page_id,
        )
        self.payees = [
            StringField(prediction, page_id=page_id)
            for prediction in raw_prediction["payees"]
        ]
        self.routing_number = StringField(
            raw_prediction["routing_number"],
            page_id=page_id,
        )

    def __str__(self) -> str:
        payees = f"\n { ' ' * 8 }".join(
            [str(item) for item in self.payees],
        )
        out_str: str = f":Check Issue Date: {self.date}\n"
        out_str += f":Amount: {self.amount}\n"
        out_str += f":Payees: {payees}\n"
        out_str += f":Routing Number: {self.routing_number}\n"
        out_str += f":Account Number: {self.account_number}\n"
        out_str += f":Check Number: {self.check_number}\n"
        return clean_out_string(out_str)
