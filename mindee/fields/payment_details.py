from typing import Optional

from mindee.fields.base import Field


class PaymentDetails(Field):
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
        payment_details_prediction: dict,
        value_key: str = "iban",
        account_number_key: str = "account_number",
        iban_key: str = "iban",
        routing_number_key: str = "routing_number",
        swift_key: str = "swift",
        reconstructed: bool = False,
        page_n=None,
    ):
        """
        Payment details field object.

        :param payment_details_prediction: Payment detail prediction object from HTTP response
        :param value_key: Corresponds to iban
        :param account_number_key: Key to use for getting the account number in the
            payment_details_prediction dict
        :param iban_key: Key to use for getting the IBAN in the payment_details_prediction dict
        :param routing_number_key: Key to use for getting the Routing number in the
            payment_details_prediction dict
        :param swift_key: Key to use for getting the SWIFT  in the payment_details_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_n: Page number for multi pages pdf
        """
        super().__init__(
            payment_details_prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_n=page_n,
        )

        try:
            assert isinstance(payment_details_prediction[account_number_key], str)
            self.account_number = str(payment_details_prediction[account_number_key])
            if self.account_number == "N/A":
                self.account_number = None
        except (KeyError, AssertionError):
            self.account_number = None

        try:
            assert isinstance(payment_details_prediction[iban_key], str)
            self.iban = str(payment_details_prediction[iban_key])
            if self.iban == "N/A":
                self.iban = None
        except (KeyError, AssertionError):
            self.iban = None

        try:
            assert isinstance(payment_details_prediction[routing_number_key], str)
            self.routing_number = str(payment_details_prediction[routing_number_key])
            if self.routing_number == "N/A":
                self.routing_number = None
        except (KeyError, AssertionError):
            self.routing_number = None

        try:
            assert isinstance(payment_details_prediction[swift_key], str)
            self.swift = str(payment_details_prediction[swift_key])
            if self.swift == "N/A":
                self.swift = None
        except (KeyError, AssertionError):
            self.swift = None

    def __str__(self) -> str:
        output_str = ""
        if self.account_number is not None:
            output_str += str(self.account_number) + "; "
        if self.iban is not None:
            output_str += str(self.iban) + "; "
        if self.routing_number is not None:
            output_str += str(self.routing_number) + "; "
        if self.swift is not None:
            output_str += str(self.swift) + "; "
        return output_str.strip()
