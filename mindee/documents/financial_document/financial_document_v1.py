from typing import List, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.amount import AmountField
from mindee.fields.classification import ClassificationField
from mindee.fields.company_registration import CompanyRegistrationField
from mindee.fields.date import DateField
from mindee.fields.locale import LocaleField
from mindee.fields.payment_details import PaymentDetails
from mindee.fields.tax import Taxes
from mindee.fields.text import TextField

from .financial_document_v1_line_item import FinancialDocumentV1LineItem


class FinancialDocumentV1(Document):
    """Financial Document v1 prediction results."""

    category: ClassificationField
    """The purchase category among predefined classes."""
    customer_address: TextField
    """The address of the customer."""
    customer_company_registrations: List[CompanyRegistrationField]
    """List of company registrations associated to the customer."""
    customer_name: TextField
    """The name of the customer."""
    date: DateField
    """The date the purchase was made."""
    document_type: ClassificationField
    """One of: 'INVOICE', 'CREDIT NOTE', 'CREDIT CARD RECEIPT', 'EXPENSE RECEIPT'."""
    due_date: DateField
    """The date on which the payment is due."""
    invoice_number: TextField
    """The invoice number or identifier."""
    line_items: List[FinancialDocumentV1LineItem]
    """List of line item details."""
    locale: LocaleField
    """The locale detected on the document."""
    reference_numbers: List[TextField]
    """List of Reference numbers, including PO number."""
    subcategory: ClassificationField
    """The purchase subcategory among predefined classes for transport and food."""
    supplier_address: TextField
    """The address of the supplier or merchant."""
    supplier_company_registrations: List[CompanyRegistrationField]
    """List of company registrations associated to the supplier."""
    supplier_name: TextField
    """The name of the supplier or merchant."""
    supplier_payment_details: List[PaymentDetails]
    """List of payment details associated to the supplier."""
    supplier_phone_number: TextField
    """The phone number of the supplier or merchant."""
    taxes: Taxes
    """List of tax lines information."""
    time: TextField
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
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        """
        Financial Document v1 prediction results.

        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type="financial_document",
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
        self.customer_address = TextField(
            api_prediction["customer_address"],
            page_id=page_n,
        )
        self.customer_company_registrations = [
            CompanyRegistrationField(prediction, page_id=page_n)
            for prediction in api_prediction["customer_company_registrations"]
        ]
        self.customer_name = TextField(
            api_prediction["customer_name"],
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
        self.due_date = DateField(
            api_prediction["due_date"],
            page_id=page_n,
        )
        self.invoice_number = TextField(
            api_prediction["invoice_number"],
            page_id=page_n,
        )
        self.line_items = [
            FinancialDocumentV1LineItem(prediction, page_id=page_n)
            for prediction in api_prediction["line_items"]
        ]
        self.locale = LocaleField(
            api_prediction["locale"],
            page_id=page_n,
        )
        self.reference_numbers = [
            TextField(prediction, page_id=page_n)
            for prediction in api_prediction["reference_numbers"]
        ]
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
        self.supplier_payment_details = [
            PaymentDetails(prediction, page_id=page_n)
            for prediction in api_prediction["supplier_payment_details"]
        ]
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
            "Financial Document V1 Prediction\n"
            "================================\n"
            f":Filename: {self.filename or ''}\n"
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
            f":Supplier Company Registrations: {supplier_company_registrations}\n"
            f":Supplier Address: {self.supplier_address}\n"
            f":Supplier Phone Number: {self.supplier_phone_number}\n"
            f":Customer name: {self.customer_name}\n"
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


TypeFinancialDocumentV1 = TypeVar(
    "TypeFinancialDocumentV1",
    bound=FinancialDocumentV1,
)
