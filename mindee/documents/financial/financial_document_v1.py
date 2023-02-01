from typing import List, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.documents.invoice.line_item import InvoiceLineItem
from mindee.fields.amount import AmountField
from mindee.fields.company_registration import CompanyRegistrationField
from mindee.fields.date import DateField
from mindee.fields.locale import LocaleField
from mindee.fields.payment_details import PaymentDetails
from mindee.fields.tax import TaxField
from mindee.fields.text import TextField


class FinancialDocumentV1(Document):
    locale: LocaleField
    """locale information"""
    total_amount: AmountField
    """Total including taxes"""
    total_net: AmountField
    """Total excluding taxes"""
    date: DateField
    """Date the invoice was issued"""
    invoice_number: TextField
    """Invoice number"""
    reference_numbers: List[TextField]
    """List of Reference numbers including PO number."""
    due_date: DateField
    """Date the invoice is due"""
    taxes: List[TaxField] = []
    """List of all taxes"""
    total_tax: AmountField
    """Sum total of all taxes"""
    supplier_name: TextField
    """Supplier 's name"""
    supplier_address: TextField
    """Supplier's address"""
    supplier_company_registrations: List[CompanyRegistrationField]
    """Company numbers"""
    customer_name: TextField
    """Customer's name"""
    customer_address: TextField
    """Customer's address"""
    customer_company_registrations: List[CompanyRegistrationField]
    """Customer company registration numbers"""
    supplier_payment_details: List[PaymentDetails]
    """Payment details"""
    line_items: List[InvoiceLineItem]
    """Details of line items"""
    tip: AmountField
    """Total amount of tip and gratuity."""
    time: TextField
    """Time as seen on the receipt in HH:MM format."""
    document_type: TextField
    """A classification field, among predefined classes."""
    category: TextField
    """The invoice or receipt category among predefined classes."""
    subcategory: TextField
    """The invoice or receipt sub-category among predefined classes."""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
        document_type="financial_doc",
    ):
        """
        Union of `Invoice` and `Receipt`.

        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi-page PDF input
        """
        # need this for building from prediction
        self.input_file = input_source

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
        self.supplier_company_registrations = [
            CompanyRegistrationField(field_dict, page_n=page_n)
            for field_dict in api_prediction["supplier_company_registrations"]
        ]
        self.date = DateField(api_prediction["date"], page_n=page_n)
        self.due_date = DateField(api_prediction["due_date"], page_n=page_n)
        self.invoice_number = TextField(api_prediction["invoice_number"], page_n=page_n)
        self.reference_numbers = [
            TextField(reference_number, page_n=page_n)
            for reference_number in api_prediction["reference_numbers"]
        ]
        self.locale = LocaleField(
            api_prediction["locale"], value_key="language", page_n=page_n
        )
        self.supplier_name = TextField(api_prediction["supplier_name"], page_n=page_n)
        self.supplier_address = TextField(
            api_prediction["supplier_address"], page_n=page_n
        )
        self.customer_name = TextField(api_prediction["customer_name"], page_n=page_n)
        self.customer_company_registrations = [
            CompanyRegistrationField(field_dict, page_n=page_n)
            for field_dict in api_prediction["customer_company_registrations"]
        ]
        self.customer_address = TextField(
            api_prediction["customer_address"], page_n=page_n
        )

        self.taxes = [
            TaxField(tax_prediction, page_n=page_n, value_key="value")
            for tax_prediction in api_prediction["taxes"]
        ]
        self.supplier_payment_details = [
            PaymentDetails(payment_detail, page_n=page_n)
            for payment_detail in api_prediction["supplier_payment_details"]
        ]
        self.line_items = [
            InvoiceLineItem(prediction=line_item, page_n=page_n)
            for line_item in api_prediction["line_items"]
        ]
        self.total_amount = AmountField(api_prediction["total_amount"], page_n=page_n)
        self.total_net = AmountField(api_prediction["total_net"], page_n=page_n)
        self.total_tax = AmountField(api_prediction["total_tax"], page_n=page_n)
        self.tip = AmountField(api_prediction["tip"], page_n=page_n)
        self.time = TextField(api_prediction["time"], page_n=page_n)
        self.document_type = TextField(api_prediction["document_type"], page_n=page_n)
        self.category = TextField(api_prediction["category"], page_n=page_n)
        self.subcategory = TextField(api_prediction["subcategory"], page_n=page_n)

    def __str__(self) -> str:
        supplier_company_registrations = "; ".join(
            [str(n.value) for n in self.supplier_company_registrations]
        )
        customer_company_registrations = "; ".join(
            [str(n.value) for n in self.customer_company_registrations]
        )
        reference_numbers = ", ".join([str(n.value) for n in self.reference_numbers])
        payment_details = "\n                          ".join(
            [str(p) for p in self.supplier_payment_details]
        )
        taxes = "\n       ".join(f"{t}" for t in self.taxes)
        line_items = "\n"
        if self.line_items:
            line_items = "\n  Code           | QTY    | Price   | Amount   | Tax (Rate)       | Description\n"
            for item in self.line_items:
                line_items += f"  {item}\n"
        return clean_out_string(
            "----- Financial Document V1 -----\n"
            f"Filename: {self.filename or ''}\n"
            f"Document type: {self.document_type}\n"
            f"Category: {self.category}\n"
            f"Subcategory: {self.subcategory}\n"
            f"Locale: {self.locale}\n"
            f"Invoice number: {self.invoice_number}\n"
            f"Reference numbers: {reference_numbers}\n"
            f"Date: {self.date}\n"
            f"Due date: {self.due_date}\n"
            f"Time: {self.time}\n"
            f"Supplier name: {self.supplier_name}\n"
            f"Supplier address: {self.supplier_address}\n"
            f"Supplier company registrations: {supplier_company_registrations}\n"
            f"Supplier payment details: {payment_details}\n"
            f"Customer name: {self.customer_name}\n"
            f"Customer address: {self.customer_address}\n"
            f"Customer company registrations: {customer_company_registrations}\n"
            f"Tip: {self.tip}\n"
            f"Taxes: {taxes}\n"
            f"Total tax: {self.total_tax}\n"
            f"Total net: {self.total_net}\n"
            f"Total amount: {self.total_amount}\n"
            f"Line Items: {line_items}"
            "----------------------"
        )

    def _checklist(self) -> None:
        pass


TypeFinancialDocumentV1 = TypeVar("TypeFinancialDocumentV1", bound=FinancialDocumentV1)
