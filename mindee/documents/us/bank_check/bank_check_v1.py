from typing import List, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.amount import AmountField
from mindee.fields.date import DateField
from mindee.fields.position import PositionField
from mindee.fields.text import TextField


class BankCheckV1(Document):
    date: DateField
    """Date the check was issued"""
    amount: AmountField
    """Total including taxes"""
    payees: List[TextField]
    """List of payees (full name or company name)"""
    check_number: TextField
    """Check number"""
    routing_number: TextField
    """Payer's bank account routing number"""
    account_number: TextField
    """Payer's bank account number"""
    check_position: PositionField
    """Check's position in the image"""
    signatures_positions: List[PositionField]
    """Signatures' positions in the image"""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
        document_type="bank_check",
    ):
        """
        Bank check document.

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
        Build the document from an API response JSON.

        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number for multi pages pdf input
        """
        self.routing_number = TextField(api_prediction["routing_number"], page_n=page_n)
        self.account_number = TextField(api_prediction["account_number"], page_n=page_n)
        self.check_number = TextField(api_prediction["check_number"], page_n=page_n)
        self.date = DateField(api_prediction["date"], page_n=page_n)
        self.amount = AmountField(api_prediction["amount"], page_n=page_n)
        self.payees = [
            TextField(payee, page_n=page_n) for payee in api_prediction["payees"]
        ]
        self.check_position = PositionField(
            api_prediction["check_position"], page_n=page_n
        )
        self.signatures_positions = [
            PositionField(signature_position, page_n=page_n)
            for signature_position in api_prediction["signatures_positions"]
        ]

    def __str__(self) -> str:
        payees = ", ".join([str(payee) for payee in self.payees])
        return clean_out_string(
            "----- US Bank Check V1 -----\n"
            f"Filename: {self.filename or ''}\n"
            f"Routing number: {self.routing_number}\n"
            f"Account number: {self.account_number}\n"
            f"Check number: {self.check_number}\n"
            f"Date: {self.date}\n"
            f"Amount: {self.amount}\n"
            f"Payees: {payees}\n"
            "----------------------"
        )

    def _checklist(self) -> None:
        pass


TypeBankCheckV1 = TypeVar("TypeBankCheckV1", bound=BankCheckV1)
