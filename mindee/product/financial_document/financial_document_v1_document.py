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
    """Financial Document API version 1.10 document data."""

    billing_address: StringField
    """The customer's address used for billing."""
    category: ClassificationField
    """The purchase category among predefined classes."""
    customer_address: StringField
    """The address of the customer."""
    customer_company_registrations: List[CompanyRegistrationField]
    """List of company registrations associated to the customer."""
    customer_id: StringField
    """The customer account number or identifier from the supplier."""
    customer_name: StringField
    """The name of the customer."""
    date: DateField
    """The date the purchase was made."""
    document_number: StringField
    """The document number or identifier."""
    document_type: ClassificationField
    """One of: 'INVOICE', 'CREDIT NOTE', 'CREDIT CARD RECEIPT', 'EXPENSE RECEIPT'."""
    due_date: DateField
    """The date on which the payment is due."""
    invoice_number: StringField
    """The invoice number or identifier only if document is an invoice."""
    line_items: List[FinancialDocumentV1LineItem]
    """List of line item details."""
    locale: LocaleField
    """The locale detected on the document."""
    payment_date: DateField
    """The date on which the payment is due / fullfilled."""
    po_number: StringField
    """The purchase order number."""
    receipt_number: StringField
    """The receipt number or identifier only if document is a receipt."""
    reference_numbers: List[StringField]
    """List of Reference numbers, including PO number."""
    shipping_address: StringField
    """The customer's address used for shipping."""
    subcategory: ClassificationField
    """The purchase subcategory among predefined classes for transport and food."""
    supplier_address: StringField
    """The address of the supplier or merchant."""
    supplier_company_registrations: List[CompanyRegistrationField]
    """List of company registrations associated to the supplier."""
    supplier_email: StringField
    """The email of the supplier or merchant."""
    supplier_name: StringField
    """The name of the supplier or merchant."""
    supplier_payment_details: List[PaymentDetailsField]
    """List of payment details associated to the supplier."""
    supplier_phone_number: StringField
    """The phone number of the supplier or merchant."""
    supplier_website: StringField
    """The website URL of the supplier or merchant."""
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
        super().__init__(raw_prediction, page_id)
        self.billing_address = StringField(
            raw_prediction["billing_address"],
            page_id=page_id,
        )
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
        self.customer_id = StringField(
            raw_prediction["customer_id"],
            page_id=page_id,
        )
        self.customer_name = StringField(
            raw_prediction["customer_name"],
            page_id=page_id,
        )
        self.date = DateField(
            raw_prediction["date"],
            page_id=page_id,
        )
        self.document_number = StringField(
            raw_prediction["document_number"],
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
        self.payment_date = DateField(
            raw_prediction["payment_date"],
            page_id=page_id,
        )
        self.po_number = StringField(
            raw_prediction["po_number"],
            page_id=page_id,
        )
        self.receipt_number = StringField(
            raw_prediction["receipt_number"],
            page_id=page_id,
        )
        self.reference_numbers = [
            StringField(prediction, page_id=page_id)
            for prediction in raw_prediction["reference_numbers"]
        ]
        self.shipping_address = StringField(
            raw_prediction["shipping_address"],
            page_id=page_id,
        )
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
        self.supplier_email = StringField(
            raw_prediction["supplier_email"],
            page_id=page_id,
        )
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
        self.supplier_website = StringField(
            raw_prediction["supplier_website"],
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
        out_str += f"+{char * 17}"
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
        out_str += " | Unit of measure"
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
        out_str += f":Purchase Order Number: {self.po_number}\n"
        out_str += f":Receipt Number: {self.receipt_number}\n"
        out_str += f":Document Number: {self.document_number}\n"
        out_str += f":Reference Numbers: {reference_numbers}\n"
        out_str += f":Purchase Date: {self.date}\n"
        out_str += f":Due Date: {self.due_date}\n"
        out_str += f":Payment Date: {self.payment_date}\n"
        out_str += f":Total Net: {self.total_net}\n"
        out_str += f":Total Amount: {self.total_amount}\n"
        out_str += f":Taxes: {self.taxes}\n"
        out_str += f":Supplier Payment Details: {supplier_payment_details}\n"
        out_str += f":Supplier Name: {self.supplier_name}\n"
        out_str += (
            f":Supplier Company Registrations: {supplier_company_registrations}\n"
        )
        out_str += f":Supplier Address: {self.supplier_address}\n"
        out_str += f":Supplier Phone Number: {self.supplier_phone_number}\n"
        out_str += f":Customer Name: {self.customer_name}\n"
        out_str += f":Supplier Website: {self.supplier_website}\n"
        out_str += f":Supplier Email: {self.supplier_email}\n"
        out_str += (
            f":Customer Company Registrations: {customer_company_registrations}\n"
        )
        out_str += f":Customer Address: {self.customer_address}\n"
        out_str += f":Customer ID: {self.customer_id}\n"
        out_str += f":Shipping Address: {self.shipping_address}\n"
        out_str += f":Billing Address: {self.billing_address}\n"
        out_str += f":Document Type: {self.document_type}\n"
        out_str += f":Purchase Subcategory: {self.subcategory}\n"
        out_str += f":Purchase Category: {self.category}\n"
        out_str += f":Total Tax: {self.total_tax}\n"
        out_str += f":Tip and Gratuity: {self.tip}\n"
        out_str += f":Purchase Time: {self.time}\n"
        out_str += f":Line Items: {self._line_items_to_str()}\n"
        return clean_out_string(out_str)
