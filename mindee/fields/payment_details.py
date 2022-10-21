from typing import Optional

from mindee.fields.base import BaseField, FieldPositionMixin, TypePrediction


class PaymentDetails(FieldPositionMixin, BaseField):
    account_number: Optional[str] = None
    """Account number"""
    iban: Optional[str] = None
    """Account IBAN"""
    routing_number: Optional[str] = None
    """Account routing number"""
    swift: Optional[str] = None
    """Bank's SWIFT code"""

    def __init__(
        self,
        prediction: TypePrediction,
        value_key: str = "iban",
        account_number_key: str = "account_number",
        iban_key: str = "iban",
        routing_number_key: str = "routing_number",
        swift_key: str = "swift",
        reconstructed: bool = False,
        page_n: Optional[int] = None,
    ):
        """
        Payment details field object.

        :param prediction: Payment detail prediction object from HTTP response
        :param value_key: Corresponds to iban
        :param account_number_key: Key to use for getting the account number in the
            payment_details_prediction dict
        :param iban_key: Key to use for getting the IBAN in the payment_details_prediction dict
        :param routing_number_key: Key to use for getting the Routing number in the
            payment_details_prediction dict
        :param swift_key: Key to use for getting the SWIFT  in the payment_details_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_n: Page number for multi-page document
        """
        super().__init__(
            prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_n=page_n,
        )

        self._set_position(prediction)

        try:
            assert isinstance(prediction[account_number_key], str)
            self.account_number = str(prediction[account_number_key])
            if self.account_number == "N/A":
                self.account_number = None
        except (KeyError, AssertionError):
            self.account_number = None

        try:
            assert isinstance(prediction[iban_key], str)
            self.iban = str(prediction[iban_key])
            if self.iban == "N/A":
                self.iban = None
        except (KeyError, AssertionError):
            self.iban = None

        try:
            assert isinstance(prediction[routing_number_key], str)
            self.routing_number = str(prediction[routing_number_key])
            if self.routing_number == "N/A":
                self.routing_number = None
        except (KeyError, AssertionError):
            self.routing_number = None

        try:
            assert isinstance(prediction[swift_key], str)
            self.swift = str(prediction[swift_key])
            if self.swift == "N/A":
                self.swift = None
        except (KeyError, AssertionError):
            self.swift = None

    def __str__(self) -> str:
        out_str = ""
        if self.account_number is not None:
            out_str += str(self.account_number) + "; "
        if self.iban is not None:
            out_str += str(self.iban) + "; "
        if self.routing_number is not None:
            out_str += str(self.routing_number) + "; "
        if self.swift is not None:
            out_str += str(self.swift) + "; "
        return out_str.strip()
