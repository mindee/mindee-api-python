from typing import List, Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.text import StringField
from mindee.product.us.us_mail.us_mail_v2_recipient_address import (
    UsMailV2RecipientAddress,
)
from mindee.product.us.us_mail.us_mail_v2_sender_address import UsMailV2SenderAddress


class UsMailV2Document(Prediction):
    """US Mail API version 2.0 document data."""

    recipient_addresses: List[UsMailV2RecipientAddress]
    """The addresses of the recipients."""
    recipient_names: List[StringField]
    """The names of the recipients."""
    sender_address: UsMailV2SenderAddress
    """The address of the sender."""
    sender_name: StringField
    """The name of the sender."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        US Mail document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction, page_id)
        self.recipient_addresses = [
            UsMailV2RecipientAddress(prediction, page_id=page_id)
            for prediction in raw_prediction["recipient_addresses"]
        ]
        self.recipient_names = [
            StringField(prediction, page_id=page_id)
            for prediction in raw_prediction["recipient_names"]
        ]
        self.sender_address = UsMailV2SenderAddress(
            raw_prediction["sender_address"],
            page_id=page_id,
        )
        self.sender_name = StringField(
            raw_prediction["sender_name"],
            page_id=page_id,
        )

    @staticmethod
    def _recipient_addresses_separator(char: str) -> str:
        out_str = "  "
        out_str += f"+{char * 17}"
        out_str += f"+{char * 37}"
        out_str += f"+{char * 19}"
        out_str += f"+{char * 13}"
        out_str += f"+{char * 24}"
        out_str += f"+{char * 7}"
        out_str += f"+{char * 27}"
        return out_str + "+"

    def _recipient_addresses_to_str(self) -> str:
        if not self.recipient_addresses:
            return ""

        lines = f"\n{self._recipient_addresses_separator('-')}\n  ".join(
            [item.to_table_line() for item in self.recipient_addresses]
        )
        out_str = ""
        out_str += f"\n{self._recipient_addresses_separator('-')}\n "
        out_str += " | City           "
        out_str += " | Complete Address                   "
        out_str += " | Is Address Change"
        out_str += " | Postal Code"
        out_str += " | Private Mailbox Number"
        out_str += " | State"
        out_str += " | Street                   "
        out_str += f" |\n{self._recipient_addresses_separator('=')}"
        out_str += f"\n  {lines}"
        out_str += f"\n{self._recipient_addresses_separator('-')}"
        return out_str

    def __str__(self) -> str:
        recipient_names = f"\n { ' ' * 17 }".join(
            [str(item) for item in self.recipient_names],
        )
        out_str: str = f":Sender Name: {self.sender_name}\n"
        out_str += f":Sender Address:\n{self.sender_address.to_field_list()}\n"
        out_str += f":Recipient Names: {recipient_names}\n"
        out_str += f":Recipient Addresses: {self._recipient_addresses_to_str()}\n"
        return clean_out_string(out_str)
