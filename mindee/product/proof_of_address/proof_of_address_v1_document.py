from typing import List, Optional

from mindee.parsing.common import Prediction, StringDict, clean_out_string
from mindee.parsing.standard import (
    CompanyRegistrationField,
    DateField,
    LocaleField,
    StringField,
)


class ProofOfAddressV1Document(Prediction):
    """Proof of Address API version 1.1 document data."""

    date: DateField
    """The date the document was issued."""
    dates: List[DateField]
    """List of dates found on the document."""
    issuer_address: StringField
    """The address of the document's issuer."""
    issuer_company_registration: List[CompanyRegistrationField]
    """List of company registrations found for the issuer."""
    issuer_name: StringField
    """The name of the person or company issuing the document."""
    locale: LocaleField
    """The locale detected on the document."""
    recipient_address: StringField
    """The address of the recipient."""
    recipient_company_registration: List[CompanyRegistrationField]
    """List of company registrations found for the recipient."""
    recipient_name: StringField
    """The name of the person or company receiving the document."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Proof of Address document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction, page_id)
        self.date = DateField(
            raw_prediction["date"],
            page_id=page_id,
        )
        self.dates = [
            DateField(prediction, page_id=page_id)
            for prediction in raw_prediction["dates"]
        ]
        self.issuer_address = StringField(
            raw_prediction["issuer_address"],
            page_id=page_id,
        )
        self.issuer_company_registration = [
            CompanyRegistrationField(prediction, page_id=page_id)
            for prediction in raw_prediction["issuer_company_registration"]
        ]
        self.issuer_name = StringField(
            raw_prediction["issuer_name"],
            page_id=page_id,
        )
        self.locale = LocaleField(
            raw_prediction["locale"],
            page_id=page_id,
        )
        self.recipient_address = StringField(
            raw_prediction["recipient_address"],
            page_id=page_id,
        )
        self.recipient_company_registration = [
            CompanyRegistrationField(prediction, page_id=page_id)
            for prediction in raw_prediction["recipient_company_registration"]
        ]
        self.recipient_name = StringField(
            raw_prediction["recipient_name"],
            page_id=page_id,
        )

    def __str__(self) -> str:
        dates = f"\n { ' ' * 7 }".join(
            [str(item) for item in self.dates],
        )
        issuer_company_registration = f"\n { ' ' * 30 }".join(
            [str(item) for item in self.issuer_company_registration],
        )
        recipient_company_registration = f"\n { ' ' * 33 }".join(
            [str(item) for item in self.recipient_company_registration],
        )
        out_str: str = f":Locale: {self.locale}\n"
        out_str += f":Issuer Name: {self.issuer_name}\n"
        out_str += f":Issuer Company Registrations: {issuer_company_registration}\n"
        out_str += f":Issuer Address: {self.issuer_address}\n"
        out_str += f":Recipient Name: {self.recipient_name}\n"
        out_str += (
            f":Recipient Company Registrations: {recipient_company_registration}\n"
        )
        out_str += f":Recipient Address: {self.recipient_address}\n"
        out_str += f":Dates: {dates}\n"
        out_str += f":Date of Issue: {self.date}\n"
        return clean_out_string(out_str)
