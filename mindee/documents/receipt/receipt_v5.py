from typing import List, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.documents.receipt.line_item_v5 import ReceiptV5LineItem
from mindee.fields.amount import AmountField
from mindee.fields.company_registration import CompanyRegistrationField
from mindee.fields.date import DateField
from mindee.fields.locale import LocaleField
from mindee.fields.tax import TaxField
from mindee.fields.text import TextField


class ReceiptV5(Document):
    locale: LocaleField
    """locale information"""
    total_amount: AmountField
    """The total amount paid including taxes, discounts, fees, tips, and gratuity."""
    date: DateField
    """The date the purchase was made."""
    time: TextField
    """Time of purchase with 24 hours formatting (HH:MM)."""
    category: TextField
    """The receipt category among predefined classes."""
    subcategory: TextField
    """The receipt sub category among predefined classes for transport and food."""
    document_type: TextField
    """Whether the document is an expense receipt or a credit card receipt."""
    supplier_name: TextField
    """The name of the supplier or merchant."""
    supplier_phone_number: TextField
    """The Phone number of the supplier or merchant."""
    supplier_address: TextField
    """The address of the supplier or merchant."""
    supplier_company_registrations: List[CompanyRegistrationField]
    """List of supplier company registrations or identifiers."""
    taxes: List[TaxField]
    """List of tax lines information including: Amount, tax rate, tax base amount and tax code."""
    total_tax: AmountField
    """The total amount of taxes."""
    total_net: AmountField
    """The total amount excluding taxes."""
    tip: AmountField
    """The total amount of tip and gratuity."""
    line_items: List[ReceiptV5LineItem]
    """Full extraction of lines, including: description, quantity, unit price and total."""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        """
        Receipt document.

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
        self.subcategory = TextField(api_prediction["subcategory"], page_n=page_n)
        self.document_type = TextField(api_prediction["document_type"], page_n=page_n)
        self.supplier_name = TextField(
            api_prediction["supplier_name"], value_key="value", page_n=page_n
        )
        self.supplier_phone_number = TextField(
            api_prediction["supplier_phone_number"], value_key="value", page_n=page_n
        )
        self.supplier_address = TextField(
            api_prediction["supplier_address"], value_key="value", page_n=page_n
        )
        self.supplier_company_registrations = [
            CompanyRegistrationField(field_dict, page_n=page_n)
            for field_dict in api_prediction["supplier_company_registrations"]
        ]
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
        self.line_items = [
            ReceiptV5LineItem(prediction=line_item, page_n=page_n)
            for line_item in api_prediction["line_items"]
        ]

    def __str__(self) -> str:
        taxes = "\n       ".join(f"{t}" for t in self.taxes)
        supplier_company_registrations = "; ".join(
            [str(n.value) for n in self.supplier_company_registrations]
        )
        line_items = "\n"
        if self.line_items:
            line_items = (
                "\n  +----------+----------+-----------+------------------------------------+"
                "\n  | Quantity | Price    | Amount    | Description                        |"
                "\n  +==========+==========+===========+====================================+"
            )
            for item in self.line_items:
                line_items += (
                    f"\n  {item}"
                    "\n  +----------+----------+-----------+------------------------------------+"
                )

        return clean_out_string(
            "Receipt V5 Prediction\n=====================\n"
            f":Filename: {self.filename or ''}\n"
            f":Expense Locale: {self.locale}\n"
            f":Total Amount: {self.total_amount}\n"
            f":Total Excluding Taxes: {self.total_net}\n"
            f":Tip and Gratuity: {self.tip}\n"
            f":Purchase Date: {self.date}\n"
            f":Purchase Time: {self.time}\n"
            f":Expense Category: {self.category}\n"
            f":Expense Sub Category: {self.subcategory}\n"
            f":Document Type: {self.document_type}\n"
            f":Supplier Name: {self.supplier_name}\n"
            f":Supplier Phone Number: {self.supplier_phone_number}\n"
            f":Supplier Address: {self.supplier_address}\n"
            f":Supplier Company Registrations: {supplier_company_registrations}\n"
            f":Line Items: {line_items}\n"
            f":Taxes: {taxes}\n"
            f":Total Taxes: {self.total_tax}\n"
        )

    def _checklist(self) -> None:
        pass


TypeReceiptV5 = TypeVar("TypeReceiptV5", bound=ReceiptV5)
