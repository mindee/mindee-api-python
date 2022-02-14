from typing import Optional
from mindee.fields.base import Field


class PaymentDetails(Field):
    account_number: Optional[str] = None
    iban: Optional[str] = None
    routing_number: Optional[str] = None
    swift: Optional[str] = None

    def __init__(
        self,
        payment_details_prediction,
        value_key="iban",
        account_number_key="account_number",
        iban_key="iban",
        routing_number_key="routing_number",
        swift_key="swift",
        reconstructed=False,
        page_n=None,
    ):
        """
        :param payment_details_prediction: Payment detail prediction object from HTTP response
        :param value_key: Corresponds to iban
        :param account_number_key: Key to use for getting the account number in the payment_details_prediction dict
        :param iban_key: Key to use for getting the IBAN in the payment_details_prediction dict
        :param routing_number_key: Key to use for getting the Routing number  in the payment_details_prediction dict
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

    def __str__(self):
        payment_str = ""
        if self.account_number is not None:
            payment_str += str(self.account_number) + "; "

        if self.iban is not None:
            payment_str += str(self.iban) + "; "

        if self.routing_number is not None:
            payment_str += str(self.routing_number) + "; "

        if self.swift is not None:
            payment_str += str(self.swift) + "; "

        return payment_str
