from typing import List, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.amount import AmountField
from mindee.fields.classification import ClassificationField
from mindee.fields.company_registration import CompanyRegistrationField
from mindee.fields.date import DateField
from mindee.fields.locale import LocaleField
from mindee.fields.tax import Taxes
from mindee.fields.text import TextField

from .receipt_v5_line_item import ReceiptV5LineItem


class ReceiptV5(Document):
    """Receipt v5 prediction results."""

    category: ClassificationField
    """The receipt category among predefined classes."""
    date: DateField
    """The date the purchase was made."""
    document_type: ClassificationField
    """Whether the document is an expense receipt or a credit card receipt."""
    line_items: List[ReceiptV5LineItem]
    """Full extraction of lines, including: description, quantity, unit price and total."""
    locale: LocaleField
    """The locale identifier in BCP 47 (RFC 5646) format: ISO language code, '-', ISO country code."""
    subcategory: ClassificationField
    """The receipt sub category among predefined classes for transport and food."""
    supplier_address: TextField
    """The address of the supplier or merchant returned as a single string."""
    supplier_company_registrations: List[CompanyRegistrationField]
    """List of supplier company registrations or identifiers."""
    supplier_name: TextField
    """The name of the supplier or merchant."""
    supplier_phone_number: TextField
    """The Phone number of the supplier or merchant returned as a single string."""
    taxes: Taxes
    """List of tax lines information including: Amount, tax rate, tax base amount and tax code."""
    time: TextField
    """Time of purchase with 24 hours formatting (HH:MM)."""
    tip: AmountField
    """The total amount of tip and gratuity."""
    total_amount: AmountField
    """The total amount paid including taxes, discounts, fees, tips, and gratuity."""
    total_net: AmountField
    """The total amount excluding taxes."""
    total_tax: AmountField
    """The total amount of taxes."""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        """
        Receipt v5 prediction results.

        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type="receipt",
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
        self.category = ClassificationField(
            api_prediction["category"],
            page_id=page_n,
        )
        self.date = DateField(
            api_prediction["date"],
            page_id=page_n,
        )
        self.document_type = ClassificationField(
            api_prediction["document_type"],
            page_id=page_n,
        )
        self.line_items = [
            ReceiptV5LineItem(prediction, page_id=page_n)
            for prediction in api_prediction["line_items"]
        ]
        self.locale = LocaleField(
            api_prediction["locale"],
            page_id=page_n,
        )
        self.subcategory = ClassificationField(
            api_prediction["subcategory"],
            page_id=page_n,
        )
        self.supplier_address = TextField(
            api_prediction["supplier_address"],
            page_id=page_n,
        )
        self.supplier_company_registrations = [
            CompanyRegistrationField(prediction, page_id=page_n)
            for prediction in api_prediction["supplier_company_registrations"]
        ]
        self.supplier_name = TextField(
            api_prediction["supplier_name"],
            page_id=page_n,
        )
        self.supplier_phone_number = TextField(
            api_prediction["supplier_phone_number"],
            page_id=page_n,
        )
        self.taxes = Taxes(api_prediction["taxes"], page_id=page_n)
        self.time = TextField(
            api_prediction["time"],
            page_id=page_n,
        )
        self.tip = AmountField(
            api_prediction["tip"],
            page_id=page_n,
        )
        self.total_amount = AmountField(
            api_prediction["total_amount"],
            page_id=page_n,
        )
        self.total_net = AmountField(
            api_prediction["total_net"],
            page_id=page_n,
        )
        self.total_tax = AmountField(
            api_prediction["total_tax"],
            page_id=page_n,
        )

    @staticmethod
    def _line_items_separator(char: str) -> str:
        out_str = "  "
        out_str += f"+{char * 38}"
        out_str += f"+{char * 10}"
        out_str += f"+{char * 14}"
        out_str += f"+{char * 12}"
        return out_str + "+"

    def _line_items_to_str(self) -> str:
        if not self.line_items:
            return ""

        lines = f"\n{self._line_items_separator('-')}\n  ".join(
            [item.to_table_line() for item in self.line_items]
        )
        out_str = ""
        out_str += f"\n{self._line_items_separator('-')}\n "
        out_str += " | Description                         "
        out_str += " | Quantity"
        out_str += " | Total Amount"
        out_str += " | Unit Price"
        out_str += f" |\n{self._line_items_separator('=')}"
        out_str += f"\n  {lines}"
        out_str += f"\n{self._line_items_separator('-')}"
        return out_str

    def __str__(self) -> str:
        supplier_company_registrations = "; ".join(
            [str(n.value) for n in self.supplier_company_registrations]
        )
        return clean_out_string(
            "Receipt V5 Prediction\n"
            "=====================\n"
            f":Filename: {self.filename or ''}\n"
            f":Expense Locale: {self.locale}\n"
            f":Expense Category: {self.category}\n"
            f":Expense Sub Category: {self.subcategory}\n"
            f":Document Type: {self.document_type}\n"
            f":Purchase Date: {self.date}\n"
            f":Purchase Time: {self.time}\n"
            f":Total Amount: {self.total_amount}\n"
            f":Total Excluding Taxes: {self.total_net}\n"
            f":Total Tax: {self.total_tax}\n"
            f":Tip and Gratuity: {self.tip}\n"
            f":Taxes: {self.taxes}\n"
            f":Supplier Name: {self.supplier_name}\n"
            f":Supplier Company Registrations: {supplier_company_registrations}\n"
            f":Supplier Address: {self.supplier_address}\n"
            f":Supplier Phone Number: {self.supplier_phone_number}\n"
            f":Line Items: {self._line_items_to_str()}\n"
        )


TypeReceiptV5 = TypeVar("TypeReceiptV5", bound=ReceiptV5)
