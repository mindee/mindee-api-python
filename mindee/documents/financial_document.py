from typing import List, Optional

from mindee.documents.base import Document
from mindee.documents.invoice import Invoice
from mindee.documents.receipt import Receipt
from mindee.fields.amount import Amount
from mindee.fields.base import Field, TypedField
from mindee.fields.date import Date
from mindee.fields.locale import Locale
from mindee.fields.orientation import Orientation
from mindee.fields.payment_details import PaymentDetails
from mindee.fields.tax import Tax
from mindee.http import Endpoint


class FinancialDocument(Document):
    locale: Locale
    """locale information"""
    total_incl: Amount
    """Total including taxes"""
    total_excl: Amount
    """Total excluding taxes"""
    date: Date
    """Date the document was issued"""
    time: Field
    """Time the document was issued"""
    invoice_number: Field
    """Invoice number"""
    due_date: Date
    """Date the invoice is due"""
    taxes: List[Tax] = []
    """List of all taxes"""
    merchant_name: Field
    """Merchant/Supplier's name"""
    supplier_address: Field
    """Merchant/Supplier's address"""
    customer_name: Field
    """Customer's name"""
    customer_address: Field
    """Customer's address"""
    customer_company_registration: List[TypedField] = []
    """Customer company registration numbers"""
    payment_details: List[PaymentDetails] = []
    """Payment details"""
    company_number: List[TypedField] = []
    """Company numbers"""
    total_tax: Amount
    """Sum total of all taxes"""

    # orientation is only present on page-level, not document-level
    orientation: Optional[Orientation] = None
    """Page orientation"""

    def __init__(
        self,
        api_prediction=None,
        input_file=None,
        page_n: Optional[int] = None,
        document_type="financial_doc",
    ):
        """
        Union of `Invoice` and `Receipt`.

        :param api_prediction: Raw prediction from HTTP response
        :param input_file: Input object
        :param page_n: Page number for multi-page PDF input
        """
        # need this for building from prediction
        self.input_file = input_file

        super().__init__(
            input_file=input_file,
            document_type=document_type,
            api_prediction=api_prediction,
            page_n=page_n,
        )

    def _build_from_api_prediction(
        self, api_prediction: dict, page_n: Optional[int] = None
    ):
        """
        Build the document from an API response JSON.

        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number for multi pages pdf input
        """
        if "invoice_number" in api_prediction.keys():
            invoice = Invoice(api_prediction, self.input_file, page_n=page_n)
            self.locale = invoice.locale
            self.total_incl = invoice.total_incl
            self.total_excl = invoice.total_excl
            self.date = invoice.invoice_date
            self.invoice_number = invoice.invoice_number
            self.due_date = invoice.due_date
            self.taxes = invoice.taxes
            self.merchant_name = invoice.supplier
            self.payment_details = invoice.payment_details
            self.company_number = invoice.company_number
            self.orientation = invoice.orientation
            self.total_tax = invoice.total_tax
            self.time = Field({"value": None, "confidence": 0.0})
            self.supplier_address = invoice.supplier_address
            self.customer_name = invoice.customer_name
            self.customer_company_registration = invoice.customer_company_registration
            self.customer_address = invoice.customer_address
        else:
            receipt = Receipt(api_prediction, self.input_file, page_n=page_n)
            self.orientation = receipt.orientation
            self.date = receipt.date
            self.due_date = receipt.date
            self.taxes = receipt.taxes
            self.locale = receipt.locale
            self.total_incl = receipt.total_incl
            self.total_excl = receipt.total_excl
            self.merchant_name = receipt.merchant_name
            self.time = receipt.time
            self.total_tax = receipt.total_tax
            self.invoice_number = Field({"value": None, "confidence": 0.0})
            self.supplier_address = Field({"value": None, "confidence": 0.0})
            self.customer_name = Field({"value": None, "confidence": 0.0})
            self.customer_address = Field({"value": None, "confidence": 0.0})

    def __str__(self) -> str:
        return (
            "-----Financial Document data-----\n"
            "Filename: %s \n"
            "Invoice number: %s \n"
            "Total amount including taxes: %s \n"
            "Total amount excluding taxes: %s \n"
            "Date: %s\n"
            "Invoice due date: %s\n"
            "Supplier name: %s\n"
            f"Supplier address: {self.supplier_address}\n"
            f"Customer name: {self.customer_name}\n"
            f"Customer company registration: {self.customer_company_registration}\n"
            f"Customer address: {self.customer_address}\n"
            "Taxes: %s\n"
            "Total taxes: %s\n"
            "----------------------"
            % (
                self.filename,
                self.invoice_number.value,
                self.total_incl.value,
                self.total_excl.value,
                self.date.value,
                self.due_date.value,
                self.merchant_name.value,
                ",".join([str(t.value) + " " + str(t.rate) + "%" for t in self.taxes]),
                self.total_tax.value,
            )
        )

    @staticmethod
    def request(
        endpoints: List[Endpoint],
        input_file,
        include_words: bool = False,
        close_file: bool = True,
    ):
        """
        Make request to prediction endpoint.

        :param input_file: Input object
        :param endpoints: Endpoints config
        :param include_words: Include Mindee vision words in http_response
        :param close_file: Whether to `close()` the file after parsing it.
        """
        if "pdf" in input_file.file_mimetype:
            # invoices is index 0, receipts 1 (this should be cleaned up)
            index = 0
        else:
            index = 1
        return endpoints[index].predict_request(input_file, include_words, close_file)

    def _checklist(self) -> None:
        """Set the validation rules."""
        self.checklist = {"taxes_match_total_incl": self.__taxes_match_total_incl()}

    # Checks
    def __taxes_match_total_incl(self) -> bool:
        """
        Check invoice rule of matching between taxes and total_incl.

        :return: True if rule matches, False otherwise
        """
        # Check taxes and total_incl exist
        if len(self.taxes) == 0 or self.total_incl.value is None:
            return False

        # Reconstruct total_incl from taxes
        total_vat = 0
        reconstructed_total = 0
        for tax in self.taxes:
            if tax.rate is not None and tax.rate != 0 and tax.value is not None:
                total_vat += tax.value
                reconstructed_total += tax.value + 100 * tax.value / tax.rate

        # Sanity check
        if total_vat <= 0:
            return False

        # Crate epsilon
        eps = 1 / (100 * total_vat)
        if (
            self.total_incl.value * (1 - eps) - 0.02
            <= reconstructed_total
            <= self.total_incl.value * (1 + eps) + 0.02
        ):
            for tax in self.taxes:
                tax.confidence = 1.0
            self.total_tax.confidence = 1.0
            self.total_incl.confidence = 1.0
            return True
        return False
