from typing import Optional

from mindee.parsing.common import Prediction, StringDict, clean_out_string
from mindee.parsing.standard import (
    AmountField,
    ClassificationField,
    DateField,
    LocaleField,
    StringField,
    Taxes,
)


class ReceiptV4Document(Prediction):
    """Document data for Receipt, API version 4."""

    locale: LocaleField
    """locale information"""
    total_amount: AmountField
    """Total including taxes"""
    date: DateField
    """Date the receipt was issued"""
    time: StringField
    """Time the receipt was issued, in HH: MM format."""
    category: ClassificationField
    """The type, or service category, of the purchase."""
    subcategory: ClassificationField
    """The receipt sub category among predefined classes."""
    document_type: ClassificationField
    """Whether the document is an expense receipt or a credit card receipt."""
    supplier: StringField
    """The merchant, or supplier, as found on the receipt."""
    taxes: Taxes
    """List of all taxes."""
    total_tax: AmountField
    """Total tax amount of the purchase."""
    total_net: AmountField
    "Total amount of the purchase excluding taxes."
    tip: AmountField
    """Total amount of tip and gratuity."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Receipt document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        self.locale = LocaleField(raw_prediction["locale"], page_id=page_id)
        self.total_amount = AmountField(raw_prediction["total_amount"], page_id=page_id)
        self.total_net = AmountField(raw_prediction["total_net"], page_id=page_id)
        self.total_tax = AmountField(raw_prediction["total_tax"], page_id=page_id)
        self.tip = AmountField(raw_prediction["tip"], page_id=page_id)
        self.date = DateField(raw_prediction["date"], page_id=page_id)
        self.category = ClassificationField(raw_prediction["category"], page_id=page_id)
        self.subcategory = ClassificationField(
            raw_prediction["subcategory"], page_id=page_id
        )
        self.document_type = ClassificationField(
            raw_prediction["document_type"], page_id=page_id
        )
        self.supplier = StringField(
            raw_prediction["supplier"], value_key="value", page_id=page_id
        )
        self.time = StringField(
            raw_prediction["time"], value_key="value", page_id=page_id
        )
        self.taxes = Taxes(raw_prediction["taxes"], page_id=page_id)

    def __str__(self) -> str:
        return clean_out_string(
            f":Locale: {self.locale}\n"
            f":Date: {self.date}\n"
            f":Category: {self.category}\n"
            f":Subcategory: {self.subcategory}\n"
            f":Document type: {self.document_type}\n"
            f":Time: {self.time}\n"
            f":Supplier name: {self.supplier}\n"
            f":Taxes: {self.taxes}\n"
            f":Total net: {self.total_net}\n"
            f":Total tax: {self.total_tax}\n"
            f":Tip: {self.tip}\n"
            f":Total amount: {self.total_amount}"
        )
