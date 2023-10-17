from typing import Optional

from mindee.parsing.common import Prediction, StringDict, clean_out_string
from mindee.parsing.standard import AmountField
from mindee.product.fr.petrol_receipt.petrol_receipt_v1_fuel import PetrolReceiptV1Fuel
from mindee.product.fr.petrol_receipt.petrol_receipt_v1_total import (
    PetrolReceiptV1Total,
)


class PetrolReceiptV1Document(Prediction):
    """Document data for Petrol Receipt, API version 1."""

    fuel: PetrolReceiptV1Fuel
    """The fuel type."""
    price: AmountField
    """The price per unit of fuel."""
    total: PetrolReceiptV1Total
    """The total amount paid."""
    volume: AmountField
    """The volume of fuel purchased."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Petrol Receipt document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        self.fuel = PetrolReceiptV1Fuel(
            raw_prediction["fuel"],
            page_id=page_id,
        )
        self.price = AmountField(
            raw_prediction["price"],
            page_id=page_id,
        )
        self.total = PetrolReceiptV1Total(
            raw_prediction["total"],
            page_id=page_id,
        )
        self.volume = AmountField(
            raw_prediction["volume"],
            page_id=page_id,
        )

    def __str__(self) -> str:
        out_str: str = f":Fuel Type:\n{self.fuel.to_field_list()}\n"
        out_str += f":Price per Unit: {self.price}\n"
        out_str += f":Volume: {self.volume}\n"
        out_str += f":Total Amount:\n{self.total.to_field_list()}\n"
        return clean_out_string(out_str)
