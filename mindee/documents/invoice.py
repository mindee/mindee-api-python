from typing import List, Optional

from mindee.documents.base import Document
from mindee.fields.amount import Amount
from mindee.fields.base import Field, TypedField, field_array_confidence
from mindee.fields.date import Date
from mindee.fields.locale import Locale
from mindee.fields.orientation import Orientation
from mindee.fields.payment_details import PaymentDetails
from mindee.fields.tax import Tax


class Invoice(Document):
    locale: Locale
    """locale information"""
    total_incl: Amount
    """Total including taxes"""
    total_excl: Amount
    """Total excluding taxes"""
    invoice_date: Date
    """Date the invoice was issued"""
    invoice_number: Field
    """Invoice number"""
    due_date: Date
    """Date the invoice is due"""
    taxes: List[Tax] = []
    """List of all taxes"""
    total_tax: Amount
    """Sum total of all taxes"""
    supplier: Field
    """Supplier 's name"""
    supplier_address: Field
    """Supplier's address"""
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
    # orientation is only present on page-level, not document-level
    orientation: Optional[Orientation] = None
    """Page orientation"""

    def __init__(
        self,
        api_prediction=None,
        input_file=None,
        page_n: Optional[int] = None,
        document_type="invoice",
    ):
        """
        Invoice document.

        :param api_prediction: Raw prediction from HTTP response
        :param input_file: Input object
        :param page_n: Page number for multi pages pdf input
        """
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
        Build the object from the prediction API JSON.

        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number for multi pages pdf input
        """
        if page_n is not None:
            self.orientation = Orientation(api_prediction["orientation"], page_n=page_n)

        self.company_number = [
            TypedField(field_dict, page_n=page_n)
            for field_dict in api_prediction["company_registration"]
        ]
        self.invoice_date = Date(
            api_prediction["date"], value_key="value", page_n=page_n
        )
        self.due_date = Date(
            api_prediction["due_date"], value_key="value", page_n=page_n
        )
        self.invoice_number = Field(api_prediction["invoice_number"], page_n=page_n)
        self.locale = Locale(
            api_prediction["locale"], value_key="language", page_n=page_n
        )
        self.supplier = Field(api_prediction["supplier"], page_n=page_n)
        self.supplier_address = Field(api_prediction["supplier_address"], page_n=page_n)
        self.customer_name = Field(api_prediction["customer"], page_n=page_n)
        self.customer_company_registration = [
            TypedField(field_dict, page_n=page_n)
            for field_dict in api_prediction["customer_company_registration"]
        ]
        self.customer_address = Field(api_prediction["customer_address"], page_n=page_n)

        self.taxes = [
            Tax(tax_prediction, page_n=page_n, value_key="value")
            for tax_prediction in api_prediction["taxes"]
        ]
        self.payment_details = [
            PaymentDetails(payment_detail, page_n=page_n)
            for payment_detail in api_prediction["payment_details"]
        ]
        self.total_incl = Amount(
            api_prediction["total_incl"], value_key="value", page_n=page_n
        )
        self.total_excl = Amount(
            api_prediction["total_excl"], value_key="value", page_n=page_n
        )
        self.total_tax = Amount(
            {"value": None, "confidence": 0.0}, value_key="value", page_n=page_n
        )

    def __str__(self) -> str:
        company_numbers = "; ".join([str(n.value) for n in self.company_number])
        customer_company_registration = "; ".join(
            [str(n.value) for n in self.customer_company_registration]
        )
        payments = ", ".join([str(p) for p in self.payment_details])
        taxes = ", ".join(f"{t}" for t in self.taxes)
        return (
            "-----Invoice data-----\n"
            f"Filename: {self.filename}\n"
            f"Invoice number: {self.invoice_number}\n"
            f"Total amount including taxes: {self.total_incl}\n"
            f"Total amount excluding taxes: {self.total_excl}\n"
            f"Invoice date: {self.invoice_date}\n"
            f"Invoice due date: {self.due_date}\n"
            f"Supplier name: {self.supplier}\n"
            f"Supplier address: {self.supplier_address}\n"
            f"Customer name: {self.customer_name}\n"
            f"Customer company registration: {customer_company_registration}\n"
            f"Customer address: {self.customer_address}\n"
            f"Payment details: {payments}\n"
            f"Company numbers: {company_numbers}\n"
            f"Taxes: {taxes}\n"
            f"Total taxes: {self.total_tax}\n"
            f"Locale: {self.locale}\n"
            "----------------------"
        )

    def _reconstruct(self) -> None:
        """Call fields reconstruction methods."""
        self.__reconstruct_total_tax_from_tax_lines()
        self.__reconstruct_total_excl_from_tcc_and_taxes()
        self.__reconstruct_total_incl_from_taxes_plus_excl()
        self.__reconstruct_total_tax_from_incl_and_excl()

    def _checklist(self) -> None:
        """Call check methods."""
        self.checklist = {
            "taxes_match_total_incl": self.__taxes_match_total_incl(),
            "taxes_match_total_excl": self.__taxes_match_total_excl(),
            "taxes_plus_total_excl_match_total_incl": self.__taxes_plus_total_excl_match_total_incl(),  # pylint: disable=line-too-long
        }

    # Checks
    def __taxes_match_total_incl(self) -> bool:
        """
        Check invoice matching rule between taxes and total_incl.

        :return: True if rule matches, False otherwise
        """
        # Ensure taxes and total_incl exist
        if not self.taxes or not self.total_incl.value:
            return False

        # Reconstruct total_incl from taxes
        total_vat = 0
        reconstructed_total = 0
        for tax in self.taxes:
            if tax.value is None or tax.rate is None or tax.rate == 0:
                return False
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
                tax.confidence = 1
            self.total_tax.confidence = 1.0
            self.total_incl.confidence = 1.0
            return True
        return False

    def __taxes_match_total_excl(self) -> bool:
        """
        Check invoice matching rule between taxes and total_excl.

        :return: True if rule matches, False otherwise
        """
        # Check taxes and total excl exist
        if len(self.taxes) == 0 or self.total_excl.value is None:
            return False

        # Reconstruct total excl from taxes
        total_vat = 0
        reconstructed_total = 0
        for tax in self.taxes:
            if tax.value is None or tax.rate is None or tax.rate == 0:
                return False
            total_vat += tax.value
            reconstructed_total += 100 * tax.value / tax.rate

        # Sanity check
        if total_vat <= 0:
            return False

        # Crate epsilon
        eps = 1 / (100 * total_vat)
        # Check that reconstructed total excl matches total excl
        if (
            self.total_excl.value * (1 - eps) - 0.02
            <= reconstructed_total
            <= self.total_excl.value * (1 + eps) + 0.02
        ):
            for tax in self.taxes:
                tax.confidence = 1
            self.total_tax.confidence = 1.0
            self.total_excl.confidence = 1.0
            return True
        return False

    def __taxes_plus_total_excl_match_total_incl(self) -> bool:
        """
        Check invoice matching rule.

        Rule is: sum(taxes) + total_excluding_taxes = total_including_taxes
        :return: True if rule matches, False otherwise
        """
        # Check total_tax, total excl and total incl exist
        if (
            self.total_excl.value is None
            or len(self.taxes) == 0
            or self.total_incl.value is None
        ):
            return False

        # Reconstruct total_incl
        total_vat = 0
        for tax in self.taxes:
            if tax.value is not None:
                total_vat += tax.value
        reconstructed_total = total_vat + self.total_excl.value

        # Sanity check
        if total_vat <= 0:
            return False

        # Check that reconstructed total incl matches total excl + taxes sum
        if (
            self.total_incl.value - 0.01
            <= reconstructed_total
            <= self.total_incl.value + 0.01
        ):
            for tax in self.taxes:
                tax.confidence = 1
            self.total_tax.confidence = 1.0
            self.total_excl.confidence = 1.0
            self.total_incl.confidence = 1.0
            return True
        return False

    # Reconstruct
    def __reconstruct_total_incl_from_taxes_plus_excl(self) -> None:
        """
        Set self.total_incl with Amount object.

        The total_incl Amount value is the sum of total_excl and sum of taxes
        The total_incl Amount confidence is the product of self.taxes probabilities
            multiplied by total_excl confidence
        """
        # Check total_tax, total excl exist and total incl is not set
        if (
            self.total_excl.value is None
            or len(self.taxes) == 0
            or self.total_incl.value is not None
        ):
            pass
        else:
            total_incl = {
                "value": sum(
                    [tax.value if tax.value is not None else 0 for tax in self.taxes]
                )
                + self.total_excl.value,
                "confidence": field_array_confidence(self.taxes)
                * self.total_excl.confidence,
            }
            self.total_incl = Amount(total_incl, value_key="value", reconstructed=True)

    def __reconstruct_total_excl_from_tcc_and_taxes(self) -> None:
        """
        Set self.total_excl with Amount object.

        The total_excl Amount value is the difference between total_incl and sum of taxes
        The total_excl Amount confidence is the product of self.taxes probabilities
            multiplied by total_incl confidence
        """
        # Check total_tax, total excl and total incl exist
        if (
            self.total_incl.value is None
            or len(self.taxes) == 0
            or self.total_excl.value is not None
        ):
            pass
        else:
            total_excl = {
                "value": self.total_incl.value
                - sum(
                    [tax.value if tax.value is not None else 0 for tax in self.taxes]
                ),
                "confidence": field_array_confidence(self.taxes)
                * self.total_incl.confidence,
            }
            self.total_excl = Amount(total_excl, value_key="value", reconstructed=True)

    def __reconstruct_total_tax_from_tax_lines(self) -> None:
        """
        Set self.total_tax with Amount object.

        The total_tax Amount value is the sum of all self.taxes value
        The total_tax Amount confidence is the product of self.taxes probabilities
        """
        if self.taxes:
            total_tax = {
                "value": sum(
                    [tax.value if tax.value is not None else 0 for tax in self.taxes]
                ),
                "confidence": field_array_confidence(self.taxes),
            }
            if total_tax["value"] > 0:
                self.total_tax = Amount(
                    total_tax, value_key="value", reconstructed=True
                )

    def __reconstruct_total_tax_from_incl_and_excl(self) -> None:
        """
        Set self.total_tax with Amount object.

        Check if the total tax was already set
        If not, set thta total tax amount to the diff of incl and excl
        """
        if (
            self.total_tax.value is not None
            or self.total_excl.value is None
            or self.total_incl.value is None
        ):
            pass
        else:

            total_tax = {
                "value": self.total_incl.value - self.total_excl.value,
                "confidence": self.total_incl.confidence * self.total_excl.confidence,
            }
            if total_tax["value"] >= 0:
                self.total_tax = Amount(
                    total_tax, value_key="value", reconstructed=True
                )
