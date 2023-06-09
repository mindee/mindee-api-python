from typing import List, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.documents.invoice import checks, reconstruct
from mindee.fields.amount import AmountField
from mindee.fields.classification import ClassificationField
from mindee.fields.company_registration import CompanyRegistrationField
from mindee.fields.date import DateField
from mindee.fields.locale import LocaleField
from mindee.fields.payment_details import PaymentDetails
from mindee.fields.tax import Taxes
from mindee.fields.text import TextField


class InvoiceV3(Document):
    """Invoice v3 prediction results."""

    locale: LocaleField
    """locale information"""
    document_type: ClassificationField
    """Whether the document is an INVOICE or a CREDIT NOTE."""
    total_amount: AmountField
    """Total including taxes. Same as ``total_incl``."""
    total_net: AmountField
    """Total excluding taxes. Same as ``total_excl``."""
    invoice_date: DateField
    """Date the invoice was issued"""
    invoice_number: TextField
    """Invoice number"""
    due_date: DateField
    """Date the invoice is due"""
    taxes: Taxes
    """List of all taxes"""
    total_tax: AmountField
    """Sum total of all taxes"""
    supplier: TextField
    """Supplier 's name"""
    supplier_address: TextField
    """Supplier's address"""
    customer_name: TextField
    """Customer's name"""
    customer_address: TextField
    """Customer's address"""
    customer_company_registration: List[CompanyRegistrationField]
    """Customer company registration numbers"""
    payment_details: List[PaymentDetails]
    """Payment details"""
    company_number: List[CompanyRegistrationField]
    """Company numbers"""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        """
        Invoice document.

        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type="invoice",
            api_prediction=api_prediction,
            page_n=page_n,
        )
        self._build_from_api_prediction(api_prediction["prediction"], page_n=page_n)
        self._checklist()
        self._reconstruct()

    def _build_from_api_prediction(
        self, api_prediction: TypeApiPrediction, page_n: Optional[int] = None
    ) -> None:
        """
        Build the object from the prediction API JSON.

        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number for multi pages pdf input
        """
        self.document_type = ClassificationField(
            api_prediction["document_type"], page_id=page_n
        )
        self.company_number = [
            CompanyRegistrationField(field_dict, page_id=page_n)
            for field_dict in api_prediction["company_registration"]
        ]
        self.invoice_date = DateField(api_prediction["date"], page_id=page_n)
        self.due_date = DateField(api_prediction["due_date"], page_id=page_n)
        self.invoice_number = TextField(
            api_prediction["invoice_number"], page_id=page_n
        )
        self.locale = LocaleField(api_prediction["locale"], page_id=page_n)
        self.supplier = TextField(api_prediction["supplier"], page_id=page_n)
        self.supplier_address = TextField(
            api_prediction["supplier_address"], page_id=page_n
        )
        self.customer_name = TextField(api_prediction["customer"], page_id=page_n)
        self.customer_company_registration = [
            CompanyRegistrationField(field_dict, page_id=page_n)
            for field_dict in api_prediction["customer_company_registration"]
        ]
        self.customer_address = TextField(
            api_prediction["customer_address"], page_id=page_n
        )
        self.taxes = Taxes(api_prediction["taxes"], page_id=page_n)
        self.payment_details = [
            PaymentDetails(payment_detail, page_id=page_n)
            for payment_detail in api_prediction["payment_details"]
        ]
        self.total_amount = AmountField(api_prediction["total_incl"], page_id=page_n)
        self.total_net = AmountField(api_prediction["total_excl"], page_id=page_n)
        self.total_tax = AmountField({"value": None, "confidence": 0.0}, page_id=page_n)

    @property
    def total_incl(self) -> AmountField:
        """Total including taxes."""
        return self.total_amount

    @total_incl.setter
    def total_incl(self, value: AmountField):
        self.total_amount = value

    @property
    def total_excl(self):
        """Total including taxes."""
        return self.total_net

    @total_excl.setter
    def total_excl(self, value: AmountField):
        self.total_net = value

    def __str__(self) -> str:
        company_numbers = "; ".join([str(n.value) for n in self.company_number])
        customer_company_registration = "; ".join(
            [str(n.value) for n in self.customer_company_registration]
        )
        payment_details = "\n                 ".join(
            [str(p) for p in self.payment_details]
        )

        return clean_out_string(
            "Invoice V3 Prediction\n"
            "=====================\n"
            f":Filename: {self.filename or ''}\n"
            f":Invoice number: {self.invoice_number}\n"
            f":Total amount: {self.total_amount}\n"
            f":Total net: {self.total_net}\n"
            f":Invoice date: {self.invoice_date}\n"
            f":Invoice due date: {self.due_date}\n"
            f":Supplier name: {self.supplier}\n"
            f":Supplier address: {self.supplier_address}\n"
            f":Customer name: {self.customer_name}\n"
            f":Customer company registration: {customer_company_registration}\n"
            f":Customer address: {self.customer_address}\n"
            f":Payment details: {payment_details}\n"
            f":Company numbers: {company_numbers}\n"
            f":Taxes: {self.taxes}\n"
            f":Total tax: {self.total_tax}\n"
            f":Locale: {self.locale}"
        )

    def _reconstruct(self) -> None:
        """Call fields reconstruction methods."""
        reconstruct.total_tax_from_tax_lines(self)
        reconstruct.total_excl_from_tcc_and_taxes(self)
        reconstruct.total_incl_from_taxes_plus_excl(self)
        reconstruct.total_tax_from_incl_and_excl(self)

    def _checklist(self) -> None:
        """Call check methods."""
        self.checklist = {
            "taxes_match_total_incl": checks.taxes_match_total_incl(self),
            "taxes_match_total_excl": checks.taxes_match_total_excl(self),
            "taxes_plus_total_excl_match_total_incl": checks.taxes_plus_total_excl_match_total_incl(
                self
            ),
        }


TypeInvoiceV3 = TypeVar("TypeInvoiceV3", bound=InvoiceV3)
