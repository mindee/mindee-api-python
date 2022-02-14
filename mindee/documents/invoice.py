from typing import List, Optional

from mindee.documents.base import Document
from mindee.fields import Field
from mindee.fields.date import Date
from mindee.fields.amount import Amount
from mindee.fields.locale import Locale
from mindee.fields.orientation import Orientation
from mindee.fields.payment_details import PaymentDetails
from mindee.fields.tax import Tax
from mindee.http import make_api_request, API_TYPE_OFF_THE_SHELF, Endpoint
from mindee.document_config import DocumentConfig


class Invoice(Document):
    locale: Locale
    total_incl: Amount
    total_excl: Amount
    invoice_date: Date
    invoice_number: Field
    due_date: Date
    taxes: List[Tax] = []
    supplier: Field
    payment_details: List[PaymentDetails] = []
    company_number: List[Field] = []
    total_tax: Amount
    # orientation is only present on page-level, not document-level
    orientation: Optional[Orientation] = None

    def __init__(
        self,
        api_prediction=None,
        input_file=None,
        locale=None,
        total_incl=None,
        total_excl=None,
        invoice_date=None,
        invoice_number=None,
        due_date=None,
        taxes=None,
        supplier=None,
        payment_details=None,
        company_number=None,
        orientation=None,
        total_tax=None,
        page_n=0,
        document_type="invoice",
    ):
        """
        :param api_prediction: Raw prediction from HTTP response
        :param input_file: Input object
        :param locale: locale value for creating Invoice object from scratch
        :param total_incl: total_incl value for creating Invoice object from scratch
        :param total_excl: total_excl value for creating Invoice object from scratch
        :param invoice_date: invoice_date value for creating Invoice object from scratch
        :param invoice_number: invoice_number value for creating Invoice object from scratch
        :param due_date: due_date value for creating Invoice object from scratch
        :param taxes: taxes value for creating Invoice object from scratch
        :param supplier: supplier value for creating Invoice object from scratch
        :param payment_details: payment_details value for creating Invoice object from scratch
        :param company_number: company_number value for creating Invoice object from scratch
        :param orientation: orientation value for creating Invoice object from scratch
        :param total_tax: total_tax value for creating Invoice object from scratch
        :param page_n: Page number for multi pages pdf input
        """
        # Invoke Document constructor
        super().__init__(
            input_file=input_file,
            document_type=document_type,
            api_prediction=api_prediction,
            page_n=page_n,
        )

        if api_prediction is not None:
            self.build_from_api_prediction(api_prediction, page_n=page_n)
        else:
            self.locale = Locale({"value": locale}, value_key="value", page_n=page_n)
            self.total_incl = Amount(
                {"value": total_incl}, value_key="value", page_n=page_n
            )
            self.invoice_date = Date(
                {"value": invoice_date}, value_key="value", page_n=page_n
            )
            self.due_date = Date({"value": due_date}, value_key="value", page_n=page_n)
            self.supplier = Field({"value": supplier}, value_key="value", page_n=page_n)
            if taxes is not None:
                self.taxes = [
                    Tax(
                        {"value": t[0], "rate": t[1]},
                        page_n=page_n,
                        value_key="value",
                        rate_key="rate",
                    )
                    for t in taxes
                ]
            self.orientation = Orientation(
                {"value": orientation}, value_key="value", page_n=page_n
            )
            self.total_tax = Amount(
                {"value": total_tax}, value_key="value", page_n=page_n
            )
            self.total_excl = Amount(
                {"value": total_excl}, value_key="value", page_n=page_n
            )
            self.invoice_number = Field(
                {"value": invoice_number}, value_key="value", page_n=page_n
            )
            self.payment_details = [
                PaymentDetails(
                    {"value": payment_details}, value_key="value", page_n=page_n
                )
            ]
            self.company_number = [
                Field({"value": company_number}, value_key="value", page_n=page_n)
            ]

        # Run checks
        self._checklist()

        # Reconstruct extra fields
        self._reconstruct()

    @staticmethod
    def get_document_config() -> DocumentConfig:
        """:return: the configuration for invoice"""
        return DocumentConfig(
            {
                "constructor": Invoice,
                "endpoints": [
                    Endpoint(
                        owner="mindee",
                        url_name="invoices",
                        version="2",
                        key_name="invoice",
                    )
                ],
                "document_type": "invoice",
                "singular_name": "invoice",
                "plural_name": "invoices",
            },
            api_type=API_TYPE_OFF_THE_SHELF,
        )

    def build_from_api_prediction(self, api_prediction: dict, page_n=0):
        """
        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number for multi pages pdf input
        :return: (void) set the object attributes with api prediction values
        """
        self.company_number = [
            Field(company_reg, extra_fields={"type"}, page_n=page_n)
            for company_reg in api_prediction["company_registration"]
        ]
        self.invoice_date = Date(
            api_prediction["date"], value_key="value", page_n=page_n
        )
        self.due_date = Date(
            api_prediction["due_date"], value_key="value", page_n=page_n
        )
        self.invoice_number = Field(api_prediction["invoice_number"], page_n=page_n)
        self.locale = Locale(
            api_prediction["locale"], value_key="language", page_n=page_n
        )
        if str(page_n) != "-1":
            self.orientation = Orientation(api_prediction["orientation"], page_n=page_n)
        self.supplier = Field(api_prediction["supplier"], page_n=page_n)
        self.taxes = [
            Tax(tax_prediction, page_n=page_n, value_key="value")
            for tax_prediction in api_prediction["taxes"]
        ]
        self.payment_details = [
            PaymentDetails(payment_detail, page_n=page_n)
            for payment_detail in api_prediction["payment_details"]
        ]
        self.total_incl = Amount(
            api_prediction["total_incl"], value_key="value", page_n=page_n
        )
        self.total_excl = Amount(
            api_prediction["total_excl"], value_key="value", page_n=page_n
        )
        self.total_tax = Amount(
            {"value": None, "confidence": 0.0}, value_key="value", page_n=page_n
        )

    def __str__(self) -> str:
        return (
            "-----Invoice data-----\n"
            "Filename: %s \n"
            "Invoice number: %s \n"
            "Total amount including taxes: %s \n"
            "Total amount excluding taxes: %s \n"
            "Invoice date: %s\n"
            "Invoice due date: %s\n"
            "Supplier name: %s\n"
            "Payment details: %s\n"
            "Taxes: %s\n"
            "Total taxes: %s\n"
            "----------------------"
            % (
                self.filename,
                self.invoice_number.value,
                self.total_incl.value,
                self.total_excl.value,
                self.invoice_date.value,
                self.due_date.value,
                self.supplier.value,
                ", ".join([str(p) for p in self.payment_details]),
                ", ".join([str(t.value) + " " + str(t.rate) + "%" for t in self.taxes]),
                self.total_tax.value,
            )
        )

    @staticmethod
    def request(endpoints: List[Endpoint], input_file, include_words=False):
        """
        Make request to expense_receipts endpoint
        :param input_file: Input object
        :param endpoints: Endpoints config
        :param include_words: Include Mindee vision words in http_response
        """
        return make_api_request(
            endpoints[0].predict_url, input_file, endpoints[0].api_key, include_words
        )

    def _reconstruct(self):
        """
        Call fields reconstruction methods
        """
        self.__reconstruct_total_tax_from_tax_lines()
        self.__reconstruct_total_excl_from_tcc_and_taxes()
        self.__reconstruct_total_incl_from_taxes_plus_excl()
        self.__reconstruct_total_tax_from_incl_and_excl()

    def _checklist(self):
        """
        Call check methods
        """
        self.checklist = {
            "taxes_match_total_incl": self.__taxes_match_total_incl(),
            "taxes_match_total_excl": self.__taxes_match_total_excl(),
            "taxes_plus_total_excl_match_total_incl": self.__taxes_plus_total_excl_match_total_incl(),
        }

    # Checks
    def __taxes_match_total_incl(self) -> bool:
        """
        Check invoice rule of matching between taxes and total_incl
        :return: True if rule matches, False otherwise
        """
        # Ensure taxes and total_incl exist
        if not self.taxes or not self.total_incl.value:
            return False

        # Reconstruct total_incl from taxes
        total_vat = 0
        reconstructed_total = 0
        for tax in self.taxes:
            if tax.value is None or tax.rate is None or tax.rate == 0:
                return False
            total_vat += tax.value
            reconstructed_total += tax.value + 100 * tax.value / tax.rate

        # Sanity check
        if total_vat <= 0:
            return False

        # Crate epsilon
        eps = 1 / (100 * total_vat)
        if (
            self.total_incl.value * (1 - eps) - 0.02
            <= reconstructed_total
            <= self.total_incl.value * (1 + eps) + 0.02
        ):
            for tax in self.taxes:
                tax.confidence = 1
            self.total_tax.confidence = 1.0
            self.total_incl.confidence = 1.0
            return True
        return False

    def __taxes_match_total_excl(self):
        """
        Check invoice rule of matching between taxes and total_excl
        :return: True if rule matches, False otherwise
        """
        # Check taxes and total excl exist
        if len(self.taxes) == 0 or self.total_excl.value is None:
            return False

        # Reconstruct total excl from taxes
        total_vat = 0
        reconstructed_total = 0
        for tax in self.taxes:
            if tax.value is None or tax.rate is None or tax.rate == 0:
                return False
            total_vat += tax.value
            reconstructed_total += 100 * tax.value / tax.rate

        # Sanity check
        if total_vat <= 0:
            return False

        # Crate epsilon
        eps = 1 / (100 * total_vat)
        # Check that reconstructed total excl matches total excl
        if (
            self.total_excl.value * (1 - eps) - 0.02
            <= reconstructed_total
            <= self.total_excl.value * (1 + eps) + 0.02
        ):
            for tax in self.taxes:
                tax.confidence = 1
            self.total_tax.confidence = 1.0
            self.total_excl.confidence = 1.0
            return True
        return False

    def __taxes_plus_total_excl_match_total_incl(self):
        """
        Check invoice rule of matching : sum(taxes) + total_excluding_taxes = total_including_taxes
        :return: True if rule matches, False otherwise
        """
        # Check total_tax, total excl and total incl exist
        if (
            self.total_excl.value is None
            or len(self.taxes) == 0
            or self.total_incl.value is None
        ):
            return False

        # Reconstruct total_incl
        total_vat = 0
        for tax in self.taxes:
            total_vat += tax.value
        reconstructed_total = total_vat + self.total_excl.value

        # Sanity check
        if total_vat <= 0:
            return False

        # Check that reconstructed total incl matches total excl + taxes sum
        if (
            self.total_incl.value - 0.01
            <= reconstructed_total
            <= self.total_incl.value + 0.01
        ):
            for tax in self.taxes:
                tax.confidence = 1
            self.total_tax.confidence = 1.0
            self.total_excl.confidence = 1.0
            self.total_incl.confidence = 1.0
            return True
        return False

    # Reconstruct
    def __reconstruct_total_incl_from_taxes_plus_excl(self):
        """
        Set self.total_incl with Amount object
        The total_incl Amount value is the sum of total_excl and sum of taxes
        The total_incl Amount confidence is the product of self.taxes probabilities multiplied by total_excl confidence
        """
        # Check total_tax, total excl exist and total incl is not set
        if (
            self.total_excl.value is None
            or len(self.taxes) == 0
            or self.total_incl.value is not None
        ):
            pass
        else:
            total_incl = {
                "value": sum(
                    [tax.value if tax.value is not None else 0 for tax in self.taxes]
                )
                + self.total_excl.value,
                "confidence": Field.array_confidence(self.taxes)
                * self.total_excl.confidence,
            }
            self.total_incl = Amount(total_incl, value_key="value", reconstructed=True)

    def __reconstruct_total_excl_from_tcc_and_taxes(self):
        """
        Set self.total_excl with Amount object
        The total_excl Amount value is the difference between total_incl and sum of taxes
        The total_excl Amount confidence is the product of self.taxes probabilities multiplied by total_incl confidence
        """
        # Check total_tax, total excl and total incl exist
        if (
            self.total_incl.value is None
            or len(self.taxes) == 0
            or self.total_excl.value is not None
        ):
            pass
        else:
            total_excl = {
                "value": self.total_incl.value
                - sum(
                    [tax.value if tax.value is not None else 0 for tax in self.taxes]
                ),
                "confidence": Field.array_confidence(self.taxes)
                * self.total_incl.confidence,
            }
            self.total_excl = Amount(total_excl, value_key="value", reconstructed=True)

    def __reconstruct_total_tax_from_tax_lines(self):
        """
        Set self.total_tax with Amount object
        The total_tax Amount value is the sum of all self.taxes value
        The total_tax Amount confidence is the product of self.taxes probabilities
        """
        if self.taxes:
            total_tax = {
                "value": sum(
                    [tax.value if tax.value is not None else 0 for tax in self.taxes]
                ),
                "confidence": Field.array_confidence(self.taxes),
            }
            if total_tax["value"] > 0:
                self.total_tax = Amount(
                    total_tax, value_key="value", reconstructed=True
                )

    def __reconstruct_total_tax_from_incl_and_excl(self):
        """
        Set self.total_tax with Amount object
        Check if the total tax was already set
        If not, set thta total tax amount to the diff of incl and excl
        """
        if (
            self.total_tax.value is not None
            or self.total_excl.value is None
            or self.total_incl.value is None
        ):
            pass
        else:

            total_tax = {
                "value": self.total_incl.value - self.total_excl.value,
                "confidence": self.total_incl.confidence * self.total_excl.confidence,
            }
            if total_tax["value"] >= 0:
                self.total_tax = Amount(
                    total_tax, value_key="value", reconstructed=True
                )
