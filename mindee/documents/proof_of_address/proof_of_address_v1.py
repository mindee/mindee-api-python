from typing import List, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.company_registration import CompanyRegistrationField
from mindee.fields.date import DateField
from mindee.fields.locale import LocaleField
from mindee.fields.text import TextField


class ProofOfAddressV1(Document):
    """Proof of Address v1 prediction results."""

    locale: LocaleField
    """The locale detected on the document."""
    issuer_name: TextField
    """The name of the person or company issuing the document."""
    issuer_company_registration: List[CompanyRegistrationField]
    """List of company registrations found for the issuer."""
    issuer_address: TextField
    """The address of the document's issuer."""
    recipient_name: TextField
    """The name of the person or company receiving the document."""
    recipient_company_registration: List[CompanyRegistrationField]
    """List of company registrations found for the recipient."""
    recipient_address: TextField
    """The address of the recipient."""
    dates: List[DateField]
    """List of dates found on the document."""
    date: DateField
    """The date the document was issued."""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        """
        Proof of Address v1 prediction results.

        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type="proof_of_address",
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
        self.locale = LocaleField(
            api_prediction["locale"],
            page_n=page_n,
        )
        self.issuer_name = TextField(
            api_prediction["issuer_name"],
            page_n=page_n,
        )
        self.issuer_company_registration = [
            CompanyRegistrationField(prediction, page_n=page_n)
            for prediction in api_prediction["issuer_company_registration"]
        ]
        self.issuer_address = TextField(
            api_prediction["issuer_address"],
            page_n=page_n,
        )
        self.recipient_name = TextField(
            api_prediction["recipient_name"],
            page_n=page_n,
        )
        self.recipient_company_registration = [
            CompanyRegistrationField(prediction, page_n=page_n)
            for prediction in api_prediction["recipient_company_registration"]
        ]
        self.recipient_address = TextField(
            api_prediction["recipient_address"],
            page_n=page_n,
        )
        self.dates = [
            DateField(prediction, page_n=page_n)
            for prediction in api_prediction["dates"]
        ]
        self.date = DateField(
            api_prediction["date"],
            page_n=page_n,
        )

    def __str__(self) -> str:
        issuer_company_registration = f"\n { ' ' * 28 }".join(
            [str(item) for item in self.issuer_company_registration],
        )
        recipient_company_registration = f"\n { ' ' * 31 }".join(
            [str(item) for item in self.recipient_company_registration],
        )
        dates = f"\n { ' ' * 6 }".join(
            [str(item) for item in self.dates],
        )
        return clean_out_string(
            "----- Proof of Address V1 -----\n"
            f"Filename: {self.filename or ''}\n"
            f"Locale: { self.locale }\n"
            f"Issuer Name: { self.issuer_name }\n"
            f"Issuer Company Registrations: { issuer_company_registration }\n"
            f"Issuer Address: { self.issuer_address }\n"
            f"Recipient Name: { self.recipient_name }\n"
            f"Recipient Company Registrations: { recipient_company_registration }\n"
            f"Recipient Address: { self.recipient_address }\n"
            f"Dates: { dates }\n"
            f"Date of Issue: { self.date }\n"
            "----------------------"
        )


TypeProofOfAddressV1 = TypeVar("TypeProofOfAddressV1", bound=ProofOfAddressV1)