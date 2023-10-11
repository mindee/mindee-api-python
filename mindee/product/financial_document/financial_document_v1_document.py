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
from mindee.product.financial_document.financial_document_v1_line_item import (
  FinancialDocumentV1LineItem,
)


class FinancialDocumentV1Document(Prediction):
    """Document data for Financial Document, API version 1."""

    category: ClassificationField
    """The purchase category among predefined classes."""
    customer_address: StringField
    """The address of the customer."""
    customer_company_registrations: List[CompanyRegistrationField]
    """List of company registrations associated to the customer."""
    customer_name: StringField
    """The name of the customer."""
    date: DateField
    """The date the purchase was made."""
    document_type: ClassificationField
    """One of: 'INVOICE', 'CREDIT NOTE', 'CREDIT CARD RECEIPT', 'EXPENSE RECEIPT'."""
    due_date: DateField
    """The date on which the payment is due."""
    invoice_number: StringField
    """The invoice number or identifier."""
    line_items: List[FinancialDocumentV1LineItem]
    """List of line item details."""
    locale: LocaleField
    """The locale detected on the document."""
    reference_numbers: List[StringField]
    """List of Reference numbers, including PO number."""
    subcategory: ClassificationField
    """The purchase subcategory among predefined classes for transport and food."""
    supplier_address: StringField
    """The address of the supplier or merchant."""
    supplier_company_registrations: List[CompanyRegistrationField]
    """List of company registrations associated to the supplier."""
    supplier_name: StringField
    """The name of the supplier or merchant."""
    supplier_payment_details: List[PaymentDetailsField]
    """List of payment details associated to the supplier."""
    supplier_phone_number: StringField
    """The phone number of the supplier or merchant."""
    taxes: Taxes
    """List of tax lines information."""
    time: StringField
    """The time the purchase was made."""
    tip: AmountField
    """The total amount of tip and gratuity"""
    total_amount: AmountField
    """The total amount paid: includes taxes, tips, fees, and other charges."""
    total_net: AmountField
    """The net amount paid: does not include taxes, fees, and discounts."""
    total_tax: AmountField
    """The total amount of taxes."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Financial Document document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        self.category = ClassificationField(
            raw_prediction["category"],
            page_id=page_id,
        )
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
            FinancialDocumentV1LineItem(prediction, page_id=page_id)
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
        self.subcategory = ClassificationField(
            raw_prediction["subcategory"],
            page_id=page_id,
        )
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
        self.supplier_phone_number = StringField(
            raw_prediction["supplier_phone_number"],
            page_id=page_id,
        )
        self.taxes = Taxes(raw_prediction["taxes"], page_id=page_id)
        self.time = StringField(
            raw_prediction["time"],
            page_id=page_id,
        )
        self.tip = AmountField(
            raw_prediction["tip"],
            page_id=page_id,
        )
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

        return clean_out_string(
            f":Locale: {self.locale}\n"
            f":Invoice Number: {self.invoice_number}\n"
            f":Reference Numbers: {reference_numbers}\n"
            f":Purchase Date: {self.date}\n"
            f":Due Date: {self.due_date}\n"
            f":Total Net: {self.total_net}\n"
            f":Total Amount: {self.total_amount}\n"
            f":Taxes: {self.taxes}\n"
            f":Supplier Payment Details: {supplier_payment_details}\n"
            f":Supplier name: {self.supplier_name}\n"
            f":Customer Name: {self.customer_name}\n"
            f":Supplier Company Registrations: {supplier_company_registrations}\n"
            f":Supplier Address: {self.supplier_address}\n"
            f":Supplier Phone Number: {self.supplier_phone_number}\n"
            f":Customer Company Registrations: {customer_company_registrations}\n"
            f":Customer Address: {self.customer_address}\n"
            f":Document Type: {self.document_type}\n"
            f":Purchase Subcategory: {self.subcategory}\n"
            f":Purchase Category: {self.category}\n"
            f":Total Tax: {self.total_tax}\n"
            f":Tip and Gratuity: {self.tip}\n"
            f":Purchase Time: {self.time}\n"
            f":Line Items: {self._line_items_to_str()}\n"
        )
