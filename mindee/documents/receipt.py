from typing import Optional, List

from mindee.documents.base import Document
from mindee.fields import Field
from mindee.fields.date import Date
from mindee.fields.amount import Amount
from mindee.fields.locale import Locale
from mindee.fields.orientation import Orientation
from mindee.fields.tax import Tax
from mindee.http import make_api_request, API_TYPE_OFF_THE_SHELF, Endpoint
from mindee.document_config import DocumentConfig


class Receipt(Document):
    locale: Locale
    total_incl: Amount
    date: Date
    category: Field
    merchant_name: Field
    time: Field
    taxes: List[Tax] = []
    total_tax: Amount
    total_excl: Amount
    # orientation is only present on page-level, not document-level
    orientation: Optional[Orientation] = None

    def __init__(
        self,
        api_prediction=None,
        input_file=None,
        locale=None,
        total_incl=None,
        date=None,
        category=None,
        merchant_name=None,
        time=None,
        taxes=None,
        orientation=None,
        total_tax=None,
        total_excl=None,
        page_n=0,
        document_type="receipt",
    ):
        """
        :param api_prediction: Raw prediction from HTTP response
        :param input_file: Input object
        :param locale: locale value for creating Receipt object from scratch
        :param total_incl: total_incl value for creating Receipt object from scratch
        :param date: date value for creating Receipt object from scratch
        :param category: category value for creating Receipt object from scratch
        :param merchant_name: merchant_name value for creating Receipt object from scratch
        :param time: time value for creating Receipt object from scratch
        :param taxes: taxes value for creating Receipt object from scratch
        :param orientation: orientation value for creating Receipt object from scratch
        :param total_tax: total_tax value for creating Receipt object from scratch
        :param total_excl: total_excl value for creating Receipt object from scratch
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
            self.date = Date({"value": date}, value_key="value", page_n=page_n)
            self.category = Field({"value": category}, value_key="value", page_n=page_n)
            self.merchant_name = Field(
                {"value": merchant_name}, value_key="value", page_n=page_n
            )
            self.time = Field({"value": time}, value_key="value", page_n=page_n)
            if taxes:
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

        # Run checks
        self._checklist()

        # Reconstruct extra fields
        self._reconstruct()

    @staticmethod
    def get_document_config() -> DocumentConfig:
        """:return: the configuration for receipt"""
        return DocumentConfig(
            {
                "constructor": Receipt,
                "endpoints": [
                    Endpoint(
                        owner="mindee",
                        url_name="expense_receipts",
                        version="3",
                        key_name="receipt",
                    )
                ],
                "document_type": "receipt",
                "singular_name": "receipt",
                "plural_name": "receipts",
            },
            api_type=API_TYPE_OFF_THE_SHELF,
        )

    def __str__(self) -> str:
        return (
            "-----Receipt data-----\n"
            "Filename: %s\n"
            "Total amount including taxes: %s \n"
            "Total amount excluding taxes: %s \n"
            "Date: %s\n"
            "Category: %s\n"
            "Time: %s\n"
            "Merchant name: %s\n"
            "Taxes: %s\n"
            "Total taxes: %s\n"
            "----------------------"
            % (
                self.filename,
                self.total_incl.value,
                self.total_excl.value,
                self.date.value,
                self.category.value,
                self.time.value,
                self.merchant_name.value,
                " - ".join([str(t) for t in self.taxes]),
                self.total_tax.value,
            )
        )

    def build_from_api_prediction(self, api_prediction, page_n=0):
        """
        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number for multi pages pdf input
        :return: (void) set the object attributes with api prediction values
        """
        self.locale = Locale(api_prediction["locale"], page_n=page_n)
        self.total_incl = Amount(
            api_prediction["total_incl"], value_key="value", page_n=page_n
        )
        self.date = Date(api_prediction["date"], value_key="value", page_n=page_n)
        self.category = Field(api_prediction["category"], page_n=page_n)
        self.merchant_name = Field(
            api_prediction["supplier"], value_key="value", page_n=page_n
        )
        self.time = Field(api_prediction["time"], value_key="value", page_n=page_n)
        self.taxes = [
            Tax(
                tax_prediction,
                page_n=page_n,
                value_key="value",
                rate_key="rate",
                code_key="code",
            )
            for tax_prediction in api_prediction["taxes"]
        ]
        if str(page_n) != "-1":
            self.orientation = Orientation(api_prediction["orientation"], page_n=page_n)
        self.total_tax = Amount(
            {"value": None, "confidence": 0.0}, value_key="value", page_n=page_n
        )
        self.total_excl = Amount(
            {"value": None, "confidence": 0.0}, value_key="value", page_n=page_n
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

    def _checklist(self):
        """
        Call check methods
        """
        self.checklist = {"taxes_match_total_incl": self.__taxes_match_total()}

    def _reconstruct(self):
        """
        Call fields reconstruction methods
        """
        self.__reconstruct_total_excl_from_tcc_and_taxes()
        self.__reconstruct_total_tax()

    # Checks
    def __taxes_match_total(self) -> bool:
        """
        Check receipt rule of matching between taxes and total_incl
        :return: True if rule matches, False otherwise
        """
        # Check taxes and total amount exist
        if len(self.taxes) == 0 or self.total_incl.value is None:
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
                tax.confidence = 1.0
            self.total_tax.confidence = 1.0
            self.total_incl.confidence = 1.0
            return True
        return False

    # Reconstruct
    def __reconstruct_total_excl_from_tcc_and_taxes(self):
        """
        Set self.total_excl with Amount object
        The total_excl Amount value is the difference between total_incl and sum of taxes
        The total_excl Amount confidence is the product of self.taxes probabilities multiplied by total_incl confidence
        """
        if self.taxes and self.total_incl.value is not None:
            total_excl = {
                "value": self.total_incl.value - Field.array_sum(self.taxes),
                "confidence": Field.array_confidence(self.taxes)
                * self.total_incl.confidence,
            }
            self.total_excl = Amount(total_excl, value_key="value", reconstructed=True)

    def __reconstruct_total_tax(self):
        """
        Set self.total_tax with Amount object
        The total_tax Amount value is the sum of all self.taxes value
        The total_tax Amount confidence is the product of self.taxes probabilities
        """
        if self.taxes and self.total_tax.value is None:
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
