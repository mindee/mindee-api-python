from typing import Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.standard.base import BaseField, FieldPositionMixin


class PaymentDetailsField(FieldPositionMixin, BaseField):
    """Information on a single payment."""

    account_number: Optional[str]
    """Account number"""
    iban: Optional[str]
    """Account IBAN"""
    routing_number: Optional[str]
    """Account routing number"""
    swift: Optional[str]
    """Bank's SWIFT code"""

    def __init__(
        self,
        raw_prediction: StringDict,
        value_key: str = "iban",
        account_number_key: str = "account_number",
        iban_key: str = "iban",
        routing_number_key: str = "routing_number",
        swift_key: str = "swift",
        reconstructed: bool = False,
        page_id: Optional[int] = None,
    ):
        """
        Payment details field object.

        :param raw_prediction: Payment detail prediction object from HTTP response
        :param value_key: Corresponds to iban
        :param account_number_key: Key to use for getting the account number in the
            payment_details_prediction dict
        :param iban_key: Key to use for getting the IBAN in the payment_details_prediction dict
        :param routing_number_key: Key to use for getting the Routing number in the
            payment_details_prediction dict
        :param swift_key: Key to use for getting the SWIFT  in the payment_details_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_id: Page number for multi-page document
        """
        super().__init__(
            raw_prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_id=page_id,
        )

        self._set_position(raw_prediction)

        try:
            assert isinstance(raw_prediction[account_number_key], str)
            self.account_number = str(raw_prediction[account_number_key])
            if self.account_number == "N/A":
                self.account_number = None
        except (KeyError, AssertionError):
            self.account_number = None

        try:
            assert isinstance(raw_prediction[iban_key], str)
            self.iban = str(raw_prediction[iban_key])
            if self.iban == "N/A":
                self.iban = None
        except (KeyError, AssertionError):
            self.iban = None

        try:
            assert isinstance(raw_prediction[routing_number_key], str)
            self.routing_number = str(raw_prediction[routing_number_key])
            if self.routing_number == "N/A":
                self.routing_number = None
        except (KeyError, AssertionError):
            self.routing_number = None

        try:
            assert isinstance(raw_prediction[swift_key], str)
            self.swift = str(raw_prediction[swift_key])
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
