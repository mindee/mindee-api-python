from typing import List, Optional

from mindee.documents.base import Document, TypeApiPrediction
from mindee.fields.amount import Amount
from mindee.fields.base import Field
from mindee.fields.date import Date
from mindee.fields.orientation import Orientation
from mindee.fields.position import Position


class BankCheck(Document):
    date: Date
    """Date the check was issued"""
    amount: Amount
    """Total including taxes"""
    payees: List[Field]
    """List of payees (full name or company name)"""
    check_number: Field
    """Check number"""
    routing_number: Field
    """Payer's bank account routing number"""
    account_number: Field
    """Payer's bank account number"""
    check_position: Field
    """Check's position in the image"""
    signatures_positions: List[Field]
    """Signatures' positions in the image"""
    # orientation is only present on page-level, not document-level
    orientation: Optional[Orientation] = None
    """Page orientation"""

    def __init__(
        self,
        api_prediction=None,
        input_file=None,
        page_n: Optional[int] = None,
        document_type="bank_check",
    ):
        """
        Bank check document.

        :param api_prediction: Raw prediction from HTTP response
        :param input_file: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_file=input_file,
            document_type=document_type,
            api_prediction=api_prediction,
            page_n=page_n,
        )

    def _build_from_api_prediction(
        self, api_prediction: TypeApiPrediction, page_n: Optional[int] = None
    ) -> None:
        """
        Build the document from an API response JSON.

        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number for multi pages pdf input
        """
        if page_n is not None:
            self.orientation = Orientation(api_prediction["orientation"], page_n=page_n)

        self.routing_number = Field(api_prediction["routing_number"], page_n=page_n)
        self.account_number = Field(api_prediction["account_number"], page_n=page_n)
        self.check_number = Field(api_prediction["check_number"], page_n=page_n)
        self.date = Date(api_prediction["date"], "value", page_n=page_n)
        self.amount = Amount(api_prediction["amount"], value_key="value", page_n=page_n)
        self.payees = [
            Field(payee, page_n=page_n) for payee in api_prediction["payees"]
        ]
        self.check_position = Position(api_prediction["check_position"], page_n=page_n)
        self.signatures_positions = [
            Position(signature_position, page_n=page_n)
            for signature_position in api_prediction["signatures_positions"]
        ]

    def __str__(self) -> str:
        payees = ", ".join(
            [payee.value if payee.value is not None else "" for payee in self.payees]
        )
        return (
            "-----Bank check data-----\n"
            f"Filename: {self.filename}\n"
            f"Routing number: {self.routing_number}\n"
            f"Account number: {self.account_number}\n"
            f"Check number: {self.check_number}\n"
            f"Date: {self.date}\n"
            f"Amount: {self.amount}\n"
            f"Payees: {payees}\n"
            "----------------------"
        )

    def _checklist(self) -> None:
        """Call check methods."""
        self.checklist = {}
