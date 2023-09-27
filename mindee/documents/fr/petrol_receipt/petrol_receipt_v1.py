from typing import Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.amount import AmountField

from .petrol_receipt_v1_fuel import PetrolReceiptV1Fuel
from .petrol_receipt_v1_total import PetrolReceiptV1Total


class PetrolReceiptV1(Document):
    """Petrol Receipt v1 prediction results."""

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
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        """
        Petrol Receipt v1 prediction results.

        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type="petrol_receipt",
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
        self.fuel = PetrolReceiptV1Fuel(
            api_prediction["fuel"],
            page_id=page_n,
        )
        self.price = AmountField(
            api_prediction["price"],
            page_id=page_n,
        )
        self.total = PetrolReceiptV1Total(
            api_prediction["total"],
            page_id=page_n,
        )
        self.volume = AmountField(
            api_prediction["volume"],
            page_id=page_n,
        )

    def __str__(self) -> str:
        return clean_out_string(
            "FR Petrol Receipt V1 Prediction\n"
            "===============================\n"
            f":Filename: {self.filename or ''}\n"
            f":Fuel Type:\n{self.fuel.to_field_list()}\n"
            f":Price per Unit: {self.price}\n"
            f":Volume: {self.volume}\n"
            f":Total Amount:\n{self.total.to_field_list()}\n"
        )


TypePetrolReceiptV1 = TypeVar(
    "TypePetrolReceiptV1",
    bound=PetrolReceiptV1,
)
