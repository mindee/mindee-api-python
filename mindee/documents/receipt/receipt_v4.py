from typing import List, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.amount import AmountField
from mindee.fields.date import DateField
from mindee.fields.locale import LocaleField
from mindee.fields.tax import TaxField
from mindee.fields.text import TextField


class ReceiptV4(Document):
    locale: LocaleField
    """locale information"""
    total_amount: AmountField
    """Total including taxes"""
    date: DateField
    """Date the receipt was issued"""
    time: TextField
    """Time the receipt was issued, in HH: MM format."""
    category: TextField
    """The type, or service category, of the purchase."""
    supplier: TextField
    """The merchant, or supplier, as found on the receipt."""
    taxes: List[TaxField]
    """List of all taxes."""
    total_tax: AmountField
    """Total tax amount of the purchase."""
    total_net: AmountField
    "Total amount of the purchase excluding taxes."
    tip: AmountField
    """Total amount of tip and gratuity."""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
        document_type="receipt",
    ):
        """
        Receipt document.

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
        self.locale = LocaleField(api_prediction["locale"], page_n=page_n)
        self.total_amount = AmountField(api_prediction["total_amount"], page_n=page_n)
        self.total_net = AmountField(api_prediction["total_net"], page_n=page_n)
        self.total_tax = AmountField(api_prediction["total_tax"], page_n=page_n)
        self.tip = AmountField(api_prediction["tip"], page_n=page_n)
        self.date = DateField(api_prediction["date"], page_n=page_n)
        self.category = TextField(api_prediction["category"], page_n=page_n)
        self.supplier = TextField(
            api_prediction["supplier"], value_key="value", page_n=page_n
        )
        self.time = TextField(api_prediction["time"], value_key="value", page_n=page_n)
        self.taxes = [
            TaxField(
                tax_prediction,
                page_n=page_n,
                value_key="value",
                rate_key="rate",
                code_key="code",
            )
            for tax_prediction in api_prediction["taxes"]
        ]

    def __str__(self) -> str:
        taxes = "\n       ".join(f"{t}" for t in self.taxes)
        return clean_out_string(
            "----- Receipt V4 -----\n"
            f"Filename: {self.filename or ''}\n"
            f"Total amount: {self.total_amount}\n"
            f"Total net: {self.total_net}\n"
            f"Tip: {self.tip}\n"
            f"Date: {self.date}\n"
            f"Category: {self.category}\n"
            f"Time: {self.time}\n"
            f"Supplier name: {self.supplier}\n"
            f"Taxes: {taxes}\n"
            f"Total taxes: {self.total_tax}\n"
            f"Locale: {self.locale}\n"
            "----------------------"
        )

    def _checklist(self) -> None:
        pass


TypeReceiptV4 = TypeVar("TypeReceiptV4", bound=ReceiptV4)
