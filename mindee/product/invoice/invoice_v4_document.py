from typing import List, Optional

from mindee.parsing.common import Prediction, StringDict, clean_out_string
from mindee.parsing.standard import (
    AmountField,
    ClassificationField,
    CompanyRegistrationField,
    DateField,
    LocaleField,
    PaymentDetailsField,
    StringField,
    Taxes,
)
from mindee.product.invoice.invoice_v4_line_item import InvoiceV4LineItem


class InvoiceV4Document(Prediction):
    """Document data for Invoice, API version 4."""

    customer_address: StringField
    """The address of the customer."""
    customer_company_registrations: List[CompanyRegistrationField]
    """List of company registrations associated to the customer."""
    customer_name: StringField
    """The name of the customer or client."""
    date: DateField
    """The date the purchase was made."""
    document_type: ClassificationField
    """One of: 'INVOICE', 'CREDIT NOTE'."""
    due_date: DateField
    """The date on which the payment is due."""
    invoice_number: StringField
    """The invoice number or identifier."""
    line_items: List[InvoiceV4LineItem]
    """List of line item details."""
    locale: LocaleField
    """The locale detected on the document."""
    reference_numbers: List[StringField]
    """List of Reference numbers, including PO number."""
    supplier_address: StringField
    """The address of the supplier or merchant."""
    supplier_company_registrations: List[CompanyRegistrationField]
    """List of company registrations associated to the supplier."""
    supplier_name: StringField
    """The name of the supplier or merchant."""
    supplier_payment_details: List[PaymentDetailsField]
    """List of payment details associated to the supplier."""
    taxes: Taxes
    """List of tax line details."""
    total_amount: AmountField
    """The total amount paid: includes taxes, tips, fees, and other charges."""
    total_net: AmountField
    """The net amount paid: does not include taxes, fees, and discounts."""
    total_tax: AmountField
    """The total tax: includes all the taxes paid for this invoice."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Invoice document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction, page_id)
        self.customer_address = StringField(
            raw_prediction["customer_address"],
            page_id=page_id,
        )
        self.customer_company_registrations = [
            CompanyRegistrationField(prediction, page_id=page_id)
            for prediction in raw_prediction["customer_company_registrations"]
        ]
        self.customer_name = StringField(
            raw_prediction["customer_name"],
            page_id=page_id,
        )
        self.date = DateField(
            raw_prediction["date"],
            page_id=page_id,
        )
        self.document_type = ClassificationField(
            raw_prediction["document_type"],
            page_id=page_id,
        )
        self.due_date = DateField(
            raw_prediction["due_date"],
            page_id=page_id,
        )
        self.invoice_number = StringField(
            raw_prediction["invoice_number"],
            page_id=page_id,
        )
        self.line_items = [
            InvoiceV4LineItem(prediction, page_id=page_id)
            for prediction in raw_prediction["line_items"]
        ]
        self.locale = LocaleField(
            raw_prediction["locale"],
            page_id=page_id,
        )
        self.reference_numbers = [
            StringField(prediction, page_id=page_id)
            for prediction in raw_prediction["reference_numbers"]
        ]
        self.supplier_address = StringField(
            raw_prediction["supplier_address"],
            page_id=page_id,
        )
        self.supplier_company_registrations = [
            CompanyRegistrationField(prediction, page_id=page_id)
            for prediction in raw_prediction["supplier_company_registrations"]
        ]
        self.supplier_name = StringField(
            raw_prediction["supplier_name"],
            page_id=page_id,
        )
        self.supplier_payment_details = [
            PaymentDetailsField(prediction, page_id=page_id)
            for prediction in raw_prediction["supplier_payment_details"]
        ]
        self.taxes = Taxes(raw_prediction["taxes"], page_id=page_id)
        self.total_amount = AmountField(
            raw_prediction["total_amount"],
            page_id=page_id,
        )
        self.total_net = AmountField(
            raw_prediction["total_net"],
            page_id=page_id,
        )
        self.total_tax = AmountField(
            raw_prediction["total_tax"],
            page_id=page_id,
        )

    @staticmethod
    def _line_items_separator(char: str) -> str:
        out_str = "  "
        out_str += f"+{char * 38}"
        out_str += f"+{char * 14}"
        out_str += f"+{char * 10}"
        out_str += f"+{char * 12}"
        out_str += f"+{char * 14}"
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
        out_str += " | Product code"
        out_str += " | Quantity"
        out_str += " | Tax Amount"
        out_str += " | Tax Rate (%)"
        out_str += " | Total Amount"
        out_str += " | Unit Price"
        out_str += f" |\n{self._line_items_separator('=')}"
        out_str += f"\n  {lines}"
        out_str += f"\n{self._line_items_separator('-')}"
        return out_str

    def __str__(self) -> str:
        customer_company_registrations = f"\n { ' ' * 32 }".join(
            [str(item) for item in self.customer_company_registrations],
        )
        reference_numbers = f"\n { ' ' * 19 }".join(
            [str(item) for item in self.reference_numbers],
        )
        supplier_company_registrations = f"\n { ' ' * 32 }".join(
            [str(item) for item in self.supplier_company_registrations],
        )
        supplier_payment_details = f"\n { ' ' * 26 }".join(
            [str(item) for item in self.supplier_payment_details],
        )
        out_str: str = f":Locale: {self.locale}\n"
        out_str += f":Invoice Number: {self.invoice_number}\n"
        out_str += f":Reference Numbers: {reference_numbers}\n"
        out_str += f":Purchase Date: {self.date}\n"
        out_str += f":Due Date: {self.due_date}\n"
        out_str += f":Total Net: {self.total_net}\n"
        out_str += f":Total Amount: {self.total_amount}\n"
        out_str += f":Total Tax: {self.total_tax}\n"
        out_str += f":Taxes: {self.taxes}\n"
        out_str += f":Supplier Payment Details: {supplier_payment_details}\n"
        out_str += f":Supplier Name: {self.supplier_name}\n"
        out_str += (
            f":Supplier Company Registrations: {supplier_company_registrations}\n"
        )
        out_str += f":Supplier Address: {self.supplier_address}\n"
        out_str += f":Customer Name: {self.customer_name}\n"
        out_str += (
            f":Customer Company Registrations: {customer_company_registrations}\n"
        )
        out_str += f":Customer Address: {self.customer_address}\n"
        out_str += f":Document Type: {self.document_type}\n"
        out_str += f":Line Items: {self._line_items_to_str()}\n"
        return clean_out_string(out_str)
