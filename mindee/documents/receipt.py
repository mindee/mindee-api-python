from typing import List, Optional

from mindee.documents.base import Document
from mindee.fields.amount import Amount
from mindee.fields.base import Field, field_array_confidence, field_array_sum
from mindee.fields.date import Date
from mindee.fields.locale import Locale
from mindee.fields.orientation import Orientation
from mindee.fields.tax import Tax


class Receipt(Document):
    locale: Locale
    """locale information"""
    total_incl: Amount
    """Total including taxes"""
    date: Date
    """Date the receipt was issued"""
    time: Field
    """Time the receipt was issued"""
    category: Field
    """Service category"""
    merchant_name: Field
    """Merchant's name"""
    taxes: List[Tax] = []
    """List of all taxes"""
    total_tax: Amount
    """Sum total of all taxes"""
    total_excl: Amount
    """Total excluding taxes"""
    # orientation is only present on page-level, not document-level
    orientation: Optional[Orientation] = None
    """Page orientation"""

    def __init__(
        self,
        api_prediction=None,
        input_file=None,
        page_n: Optional[int] = None,
        document_type="receipt",
    ):
        """
        Receipt document.

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

    def __str__(self) -> str:
        taxes = ", ".join(f"{t}" for t in self.taxes)
        return (
            "-----Receipt data-----\n"
            f"Filename: {self.filename}\n"
            f"Total amount including taxes: {self.total_incl}\n"
            f"Total amount excluding taxes: {self.total_excl}\n"
            f"Date: {self.date}\n"
            f"Category: {self.category}\n"
            f"Time: {self.time}\n"
            f"Merchant name: {self.merchant_name}\n"
            f"Taxes: {taxes}\n"
            f"Total taxes: {self.total_tax}\n"
            f"Locale: {self.locale}\n"
            "----------------------"
        )

    def _build_from_api_prediction(
        self, api_prediction: dict, page_n: Optional[int] = None
    ):
        """
        Build the document from an API response JSON.

        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number for multi pages pdf input
        """
        if page_n is not None:
            self.orientation = Orientation(api_prediction["orientation"], page_n=page_n)

        self.locale = Locale(api_prediction["locale"], page_n=page_n)
        self.total_incl = Amount(
            api_prediction["total_incl"], value_key="value", page_n=page_n
        )
        self.date = Date(api_prediction["date"], value_key="value", page_n=page_n)
        self.category = Field(api_prediction["category"], page_n=page_n)
        self.merchant_name = Field(
            api_prediction["supplier"], value_key="value", page_n=page_n
        )
        self.time = Field(api_prediction["time"], value_key="value", page_n=page_n)
        self.taxes = [
            Tax(
                tax_prediction,
                page_n=page_n,
                value_key="value",
                rate_key="rate",
                code_key="code",
            )
            for tax_prediction in api_prediction["taxes"]
        ]
        self.total_tax = Amount(
            {"value": None, "confidence": 0.0}, value_key="value", page_n=page_n
        )
        self.total_excl = Amount(
            {"value": None, "confidence": 0.0}, value_key="value", page_n=page_n
        )

    def _checklist(self) -> None:
        """Call check methods."""
        self.checklist = {"taxes_match_total_incl": self.__taxes_match_total()}

    def _reconstruct(self) -> None:
        """Call fields reconstruction methods."""
        self.__reconstruct_total_excl_from_tcc_and_taxes()
        self.__reconstruct_total_tax()

    # Checks
    def __taxes_match_total(self) -> bool:
        """
        Check receipt rule of matching between taxes and total_incl.

        :return: True if rule matches, False otherwise
        """
        # Check taxes and total amount exist
        if len(self.taxes) == 0 or self.total_incl.value is None:
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
                tax.confidence = 1.0
            self.total_tax.confidence = 1.0
            self.total_incl.confidence = 1.0
            return True
        return False

    # Reconstruct
    def __reconstruct_total_excl_from_tcc_and_taxes(self) -> None:
        """
        Set self.total_excl with Amount object.

        The total_excl Amount value is the difference between total_incl and sum of taxes
        The total_excl Amount confidence is the product of self.taxes probabilities
            multiplied by total_incl confidence
        """
        if self.taxes and self.total_incl.value is not None:
            total_excl = {
                "value": self.total_incl.value - field_array_sum(self.taxes),
                "confidence": field_array_confidence(self.taxes)
                * self.total_incl.confidence,
            }
            self.total_excl = Amount(total_excl, value_key="value", reconstructed=True)

    def __reconstruct_total_tax(self) -> None:
        """
        Set self.total_tax with Amount object.

        The total_tax Amount value is the sum of all self.taxes value
        The total_tax Amount confidence is the product of self.taxes probabilities
        """
        if self.taxes and self.total_tax.value is None:
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
