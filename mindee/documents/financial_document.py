from typing import List

from mindee.fields import Field
from mindee.http import Endpoint
from mindee.documents.base import Document
from mindee.documents.invoice import Invoice
from mindee.documents.receipt import Receipt


class FinancialDocument(Document):
    def __init__(
        self,
        api_prediction=None,
        input_file=None,
        page_n=0,
        document_type="financial_doc",
    ):
        """
        :param api_prediction: Raw prediction from HTTP response
        :param input_file: Input object
        :param page_n: Page number for multi pages pdf input
        """
        self.locale = None
        self.total_incl = None
        self.total_excl = None
        self.date = None
        self.invoice_number = None
        self.due_date = None
        self.taxes = []
        self.merchant_name = None
        self.payment_details = None
        self.company_number = None
        self.vat_number = None
        self.orientation = None
        self.total_tax = None
        self.time = None

        # need this for building from prediction
        self.input_file = input_file

        super().__init__(
            input_file=input_file,
            document_type=document_type,
            api_prediction=api_prediction,
            page_n=page_n,
        )

    def build_from_api_prediction(self, api_prediction, page_n=0):
        """
        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number for multi pages pdf input
        :return: (void) set the object attributes with api prediction values
        """
        if "invoice_number" in api_prediction.keys():
            invoice = Invoice(api_prediction, self.input_file, page_n=page_n)
            self.locale = invoice.locale
            self.total_incl = invoice.total_incl
            self.total_excl = invoice.total_excl
            self.date = invoice.invoice_date
            self.invoice_number = invoice.invoice_number
            self.due_date = invoice.due_date
            self.taxes = invoice.taxes
            self.merchant_name = invoice.supplier
            self.payment_details = invoice.payment_details
            self.company_number = invoice.company_number
            self.orientation = invoice.orientation
            self.total_tax = invoice.total_tax
            self.time = Field({"value": None, "confidence": 0.0})
        else:
            receipt = Receipt(api_prediction, self.input_file, page_n=page_n)
            self.orientation = receipt.orientation
            self.date = receipt.date
            self.due_date = receipt.date
            self.taxes = receipt.taxes
            self.locale = receipt.locale
            self.total_incl = receipt.total_incl
            self.total_excl = receipt.total_excl
            self.merchant_name = receipt.merchant_name
            self.time = receipt.time
            self.total_tax = receipt.total_tax
            self.invoice_number = Field({"value": None, "confidence": 0.0})
            self.payment_details = []
            self.company_number = []

    def __str__(self) -> str:
        return (
            "-----Financial Document data-----\n"
            "Filename: %s \n"
            "Invoice number: %s \n"
            "Total amount including taxes: %s \n"
            "Total amount excluding taxes: %s \n"
            "Date: %s\n"
            "Invoice due date: %s\n"
            "Supplier name: %s\n"
            "Taxes: %s\n"
            "Total taxes: %s\n"
            "----------------------"
            % (
                self.filename,
                self.invoice_number.value,
                self.total_incl.value,
                self.total_excl.value,
                self.date.value,
                self.due_date.value,
                self.merchant_name.value,
                ",".join([str(t.value) + " " + str(t.rate) + "%" for t in self.taxes]),
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
        if "pdf" in input_file.file_extension:
            # invoices is index 0, receipts 1 (this should be cleaned up)
            index = 0
        else:
            index = 1
        return endpoints[index].predict_request(input_file, include_words)

    def _checklist(self):
        """
        :return: Set of validation rules
        """
        self.checklist = {"taxes_match_total_incl": self.__taxes_match_total_incl()}

    # Checks
    def __taxes_match_total_incl(self):
        """
        Check invoice rule of matching between taxes and total_incl
        :return: True if rule matches, False otherwise
        """
        # Check taxes and total_incl exist
        if len(self.taxes) == 0 or self.total_incl.value is None:
            return False

        # Reconstruct total_incl from taxes
        total_vat = 0
        reconstructed_total = 0
        for tax in self.taxes:
            if tax.rate is not None and tax.rate != 0 and tax.value is not None:
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
