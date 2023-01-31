from typing import List, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.company_registration import CompanyRegistrationField
from mindee.fields.date import DateField
from mindee.fields.locale import LocaleField
from mindee.fields.text import TextField


class ProofOfAddressV1(Document):
    locale: LocaleField
    """locale information"""
    date: DateField
    """ISO date yyyy-mm-dd. Works both for European and US dates."""
    dates: List[DateField] = []
    """All extracted ISO date yyyy-mm-dd"""
    issuer_address: TextField
    """Address of the document's issuer."""
    issuer_company_registration: List[CompanyRegistrationField] = []
    """Generic: VAT NUMBER, TAX ID, COMPANY REGISTRATION NUMBER or country specific."""
    issuer_name: TextField
    """Name of the person or company issuing the document."""
    recipient_address: TextField
    """Address of the recipient."""
    recipient_company_registration: List[CompanyRegistrationField] = []
    """Generic: VAT NUMBER, TAX ID, COMPANY REGISTRATION NUMBER or country specific."""
    recipient_name: TextField
    """Name of the document's recipient."""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
        document_type="proof_of_address",
    ):
        """
        Proof of Address document.

        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type=document_type,
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
        :param page_n: Page number for multi pages pdf input
        """
        self.locale = LocaleField(
            api_prediction["locale"], value_key="language", page_n=page_n
        )
        self.date = DateField(api_prediction["date"], page_n=page_n)
        self.dates = [
            DateField(tax_prediction, page_n=page_n)
            for tax_prediction in api_prediction["dates"]
        ]
        self.issuer_name = TextField(api_prediction["issuer_name"], page_n=page_n)
        self.issuer_address = TextField(api_prediction["issuer_address"], page_n=page_n)
        self.issuer_company_registration = [
            CompanyRegistrationField(tax_prediction, page_n=page_n)
            for tax_prediction in api_prediction["issuer_company_registration"]
        ]
        self.recipient_name = TextField(api_prediction["recipient_name"], page_n=page_n)
        self.recipient_address = TextField(
            api_prediction["recipient_address"], page_n=page_n
        )
        self.recipient_company_registration = [
            CompanyRegistrationField(tax_prediction, page_n=page_n)
            for tax_prediction in api_prediction["recipient_company_registration"]
        ]

    def __str__(self) -> str:
        issuer_company_registrations = "; ".join(
            [str(n.value) for n in self.issuer_company_registration]
        )
        recipient_company_registrations = "; ".join(
            [str(n.value) for n in self.recipient_company_registration]
        )
        dates = "\n       ".join([str(n.value) for n in self.dates])
        return clean_out_string(
            "----- Proof of Address V1 -----\n"
            f"Filename: {self.filename or ''}\n"
            f"Locale: {self.locale}\n"
            f"Issuer name: {self.issuer_name}\n"
            f"Issuer Address: {self.issuer_address}\n"
            f"Issuer Company Registrations: {issuer_company_registrations}\n"
            f"Recipient name: {self.recipient_name}\n"
            f"Recipient Address: {self.recipient_address}\n"
            f"Recipient Company Registrations: {recipient_company_registrations}\n"
            f"Issuance Date: {self.date}\n"
            f"Dates: {dates}\n"
            "----------------------"
        )

    def _checklist(self) -> None:
        pass


TypeProofOfAddressV1 = TypeVar("TypeProofOfAddressV1", bound=ProofOfAddressV1)
