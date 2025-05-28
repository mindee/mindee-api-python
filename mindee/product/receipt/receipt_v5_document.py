from typing import List, Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.amount import AmountField
from mindee.parsing.standard.classification import ClassificationField
from mindee.parsing.standard.company_registration import CompanyRegistrationField
from mindee.parsing.standard.date import DateField
from mindee.parsing.standard.locale import LocaleField
from mindee.parsing.standard.tax import Taxes
from mindee.parsing.standard.text import StringField
from mindee.product.receipt.receipt_v5_line_item import ReceiptV5LineItem


class ReceiptV5Document(Prediction):
    """Receipt API version 5.4 document data."""

    category: ClassificationField
    """The purchase category of the receipt."""
    date: DateField
    """The date the purchase was made."""
    document_type: ClassificationField
    """The type of receipt: EXPENSE RECEIPT or CREDIT CARD RECEIPT."""
    line_items: List[ReceiptV5LineItem]
    """List of all line items on the receipt."""
    locale: LocaleField
    """The locale of the document."""
    receipt_number: StringField
    """The receipt number or identifier."""
    subcategory: ClassificationField
    """The purchase subcategory of the receipt for transport and food."""
    supplier_address: StringField
    """The address of the supplier or merchant."""
    supplier_company_registrations: List[CompanyRegistrationField]
    """List of company registration numbers associated to the supplier."""
    supplier_name: StringField
    """The name of the supplier or merchant."""
    supplier_phone_number: StringField
    """The phone number of the supplier or merchant."""
    taxes: Taxes
    """The list of taxes present on the receipt."""
    time: StringField
    """The time the purchase was made."""
    tip: AmountField
    """The total amount of tip and gratuity."""
    total_amount: AmountField
    """The total amount paid: includes taxes, discounts, fees, tips, and gratuity."""
    total_net: AmountField
    """The net amount paid: does not include taxes, fees, and discounts."""
    total_tax: AmountField
    """The sum of all taxes."""

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
        super().__init__(raw_prediction, page_id)
        self.category = ClassificationField(
            raw_prediction["category"],
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
        self.line_items = [
            ReceiptV5LineItem(prediction, page_id=page_id)
            for prediction in raw_prediction["line_items"]
        ]
        self.locale = LocaleField(
            raw_prediction["locale"],
            page_id=page_id,
        )
        self.receipt_number = StringField(
            raw_prediction["receipt_number"],
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
        self.supplier_name = StringField(
            raw_prediction["supplier_name"],
            page_id=page_id,
        )
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
        out_str += f"+{char * 10}"
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
        out_str += " | Quantity"
        out_str += " | Total Amount"
        out_str += " | Unit Price"
        out_str += f" |\n{self._line_items_separator('=')}"
        out_str += f"\n  {lines}"
        out_str += f"\n{self._line_items_separator('-')}"
        return out_str

    def __str__(self) -> str:
        supplier_company_registrations = f"\n { ' ' * 32 }".join(
            [str(item) for item in self.supplier_company_registrations],
        )
        out_str: str = f":Expense Locale: {self.locale}\n"
        out_str += f":Purchase Category: {self.category}\n"
        out_str += f":Purchase Subcategory: {self.subcategory}\n"
        out_str += f":Document Type: {self.document_type}\n"
        out_str += f":Purchase Date: {self.date}\n"
        out_str += f":Purchase Time: {self.time}\n"
        out_str += f":Total Amount: {self.total_amount}\n"
        out_str += f":Total Net: {self.total_net}\n"
        out_str += f":Total Tax: {self.total_tax}\n"
        out_str += f":Tip and Gratuity: {self.tip}\n"
        out_str += f":Taxes: {self.taxes}\n"
        out_str += f":Supplier Name: {self.supplier_name}\n"
        out_str += (
            f":Supplier Company Registrations: {supplier_company_registrations}\n"
        )
        out_str += f":Supplier Address: {self.supplier_address}\n"
        out_str += f":Supplier Phone Number: {self.supplier_phone_number}\n"
        out_str += f":Receipt Number: {self.receipt_number}\n"
        out_str += f":Line Items: {self._line_items_to_str()}\n"
        return clean_out_string(out_str)
