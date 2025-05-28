from typing import Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.amount import AmountField
from mindee.parsing.standard.date import DateField
from mindee.parsing.standard.text import StringField


class DeliveryNoteV1Document(Prediction):
    """Delivery note API version 1.2 document data."""

    customer_address: StringField
    """The address of the customer receiving the goods."""
    customer_name: StringField
    """The name of the customer receiving the goods."""
    delivery_date: DateField
    """The date on which the delivery is scheduled to arrive."""
    delivery_number: StringField
    """A unique identifier for the delivery note."""
    supplier_address: StringField
    """The address of the supplier providing the goods."""
    supplier_name: StringField
    """The name of the supplier providing the goods."""
    total_amount: AmountField
    """The total monetary value of the goods being delivered."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Delivery note document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction, page_id)
        self.customer_address = StringField(
            raw_prediction["customer_address"],
            page_id=page_id,
        )
        self.customer_name = StringField(
            raw_prediction["customer_name"],
            page_id=page_id,
        )
        self.delivery_date = DateField(
            raw_prediction["delivery_date"],
            page_id=page_id,
        )
        self.delivery_number = StringField(
            raw_prediction["delivery_number"],
            page_id=page_id,
        )
        self.supplier_address = StringField(
            raw_prediction["supplier_address"],
            page_id=page_id,
        )
        self.supplier_name = StringField(
            raw_prediction["supplier_name"],
            page_id=page_id,
        )
        self.total_amount = AmountField(
            raw_prediction["total_amount"],
            page_id=page_id,
        )

    def __str__(self) -> str:
        out_str: str = f":Delivery Date: {self.delivery_date}\n"
        out_str += f":Delivery Number: {self.delivery_number}\n"
        out_str += f":Supplier Name: {self.supplier_name}\n"
        out_str += f":Supplier Address: {self.supplier_address}\n"
        out_str += f":Customer Name: {self.customer_name}\n"
        out_str += f":Customer Address: {self.customer_address}\n"
        out_str += f":Total Amount: {self.total_amount}\n"
        return clean_out_string(out_str)
