from mindee.benchmark import Benchmark

from mindee.fields.amount import Amount
from mindee.fields.date import Date
from mindee.fields.locale import Locale
from mindee.fields.orientation import Orientation
from mindee.fields.tax import Tax
from mindee.documents import Document
from mindee.fields import Field
from mindee.http import request
from mindee.documents.invoice import Invoice
from mindee.documents.receipt import Receipt
import os


class FinancialDocument(Document):
    def __init__(
            self,
            api_prediction=None,
            input_file=None,
            locale=None,
            total_incl=None,
            total_excl=None,
            date=None,
            invoice_number=None,
            due_date=None,
            taxes=None,
            merchant_name=None,
            payment_details=None,
            company_number=None,
            vat_number=None,
            orientation=None,
            total_tax=None,
            time=None,
            page_n=0
    ):
        """
        :param api_prediction: Raw prediction from HTTP response
        :param input_file: Input object
        :param locale: locale value for creating FinancialDocument object from scratch
        :param total_incl: total_incl value for creating FinancialDocument object from scratch
        :param total_excl: total_excl value for creating FinancialDocument object from scratch
        :param date: date value for creating FinancialDocument object from scratch
        :param invoice_number: invoice_number value for creating FinancialDocument object from scratch
        :param due_date: due_date value for creating FinancialDocument object from scratch
        :param taxes: taxes value for creating FinancialDocument object from scratch
        :param merchant_name: merchant_name value for creating FinancialDocument object from scratch
        :param payment_details: payment_details value for creating FinancialDocument object from scratch
        :param company_number: company_number value for creating FinancialDocument object from scratch
        :param vat_number: vat_number value for creating FinancialDocument object from scratch
        :param orientation: orientation value for creating FinancialDocument object from scratch
        :param total_tax: total_tax value for creating FinancialDocument object from scratch
        :param time: time value for creating FinancialDocument object from scratch
        :param page_n: Page number for multi pages pdf input
        """
        self.type = "FinancialDocument"
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

        if api_prediction is not None:
            self.build_from_api_prediction(api_prediction, input_file, page_n=page_n)
        else:
            self.orientation = Orientation({"value": orientation}, value_key="value", page_n=page_n)
            self.locale = Locale({"value": locale}, value_key="value", page_n=page_n)
            self.date = Date({"value": date}, value_key="value", page_n=page_n)
            self.due_date = Date({"value": due_date}, value_key="value", page_n=page_n)
            if taxes is not None:
                self.taxes = [
                    Tax({"value": t[0], "rate": t[1]}, page_n=page_n, value_key="value", rate_key="rate")
                    for t in taxes]
            self.total_incl = Amount({"value": total_incl}, value_key="value", page_n=page_n)
            self.total_excl = Amount({"value": total_excl}, value_key="value", page_n=page_n)
            self.merchant_name = Field({"value": merchant_name}, value_key="value", page_n=page_n)
            self.time = Field({"value": time}, value_key="value", page_n=page_n)
            self.total_tax = Amount({"value": total_tax}, value_key="value", page_n=page_n)
            self.vat_number = Field({"value": vat_number}, value_key="value", page_n=page_n)
            self.invoice_number = Field({"value": invoice_number}, value_key="value", page_n=page_n)
            self.payment_details = Field({"value": payment_details}, value_key="value", page_n=page_n)
            self.company_number = Field({"value": company_number}, value_key="value", page_n=page_n)

        # Invoke Document constructor
        super(FinancialDocument, self).__init__(input_file)

        # Run checks
        self._checklist()

        # Reconstruct extra fields
        self._reconstruct()

    def build_from_api_prediction(self, api_prediction, input_file, page_n=0):
        """
        :param api_prediction: Raw prediction from HTTP response
        :param input_file: Input object
        :param page_n: Page number for multi pages pdf input
        :return: (void) set the object attributes with api prediction values
        """
        if "invoice_number" in api_prediction.keys():
            invoice = Invoice(api_prediction, input_file, page_n=page_n)
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
            self.time = Field({"value": None, "probability": 0.})
        else:
            receipt = Receipt(api_prediction, input_file, page_n=page_n)
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
            self.invoice_number = Field({"value": None, "probability": 0.})
            self.payment_details = Field({"value": None, "probability": 0.})
            self.company_number = Field({"value": None, "probability": 0.})

    def __str__(self):
        return "-----Financial document-----\n" \
               "Filename: %s \n" \
               "Total amount: %s \n" \
               "Date: %s\n" \
               "Merchant name: %s\n" \
               "Total taxes: %s\n" \
               "----------------------" % \
               (
                   self.filename,
                   self.total_incl.value,
                   self.date.value,
                   self.merchant_name.value,
                   self.total_tax.value
               )

    @staticmethod
    def compare(financial_document=None, ground_truth=None):
        """
        :param financial_document: FinancialDocument object to compare
        :param ground_truth: Ground truth FinancialDocument object
        :return: Accuracy and precisions metrics
        """
        assert financial_document is not None
        assert ground_truth is not None
        assert isinstance(financial_document, FinancialDocument)
        assert isinstance(ground_truth, FinancialDocument)

        metrics = {}

        # Compute Accuracy metrics
        metrics.update(FinancialDocument.compute_accuracy(financial_document, ground_truth))

        # Compute precision metrics
        metrics.update(FinancialDocument.compute_precision(financial_document, ground_truth))

        return metrics

    @staticmethod
    def request(
            input_file,
            base_url,
            expense_receipt_token=None,
            invoice_token=None,
            include_words=False
    ):
        """
        Make request to invoices endpoint if .pdf, expense_receipts otherwise
        :param include_words: Bool, extract all words into http_response
        :param input_file: Input object
        :param base_url: API base URL
        :param expense_receipt_token: Expense receipts API token
        :param invoice_token: Invoices API token
        """
        if "pdf" in input_file.file_extension:
            url = os.path.join(base_url, "invoices", "v2", "predict")
            return request(url, input_file, invoice_token, include_words)
        else:
            url = os.path.join(base_url, "expense_receipts", "v3", "predict")
            return request(url, input_file, expense_receipt_token, include_words)

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
            if tax.rate is not None and tax.rate != 0:
                total_vat += tax.value
                reconstructed_total += tax.value + 100 * tax.value / tax.rate

        # Sanity check
        if total_vat <= 0:
            return False

        # Crate epsilon
        eps = 1 / (100 * total_vat)

        if self.total_incl.value * (1 - eps) - 0.02 <= reconstructed_total <= self.total_incl.value * (
                1 + eps) + 0.02:
            for tax in self.taxes:
                tax.probability = 1
            self.total_tax.probability = 1.
            self.total_incl.probability = 1.
            return True
        else:
            return False

    @staticmethod
    def compute_accuracy(financial_document, ground_truth):
        """
        :param financial_document: FinancialDocument object to compare
        :param ground_truth: Ground truth FinancialDocument object
        :return: Accuracy metrics
        """
        return {
            "__acc__total_incl": ground_truth.total_incl == financial_document.total_incl,
            "__acc__total_excl": ground_truth.total_excl == financial_document.total_excl,
            "__acc__invoice_date": ground_truth.date == financial_document.date,
            "__acc__invoice_number": ground_truth.invoice_number == financial_document.invoice_number,
            "__acc__due_date": ground_truth.due_date == financial_document.due_date,
            "__acc__total_tax": ground_truth.total_tax == financial_document.total_tax,
            "__acc__taxes": Tax.compare_arrays(financial_document.taxes, ground_truth.taxes),
        }

    @staticmethod
    def compute_precision(financial_document, ground_truth):
        """
        :param financial_document: FinancialDocument object to compare
        :param ground_truth: Ground truth FinancialDocument object
        :return: Precision metrics
        """
        precisions = {
            "__pre__total_incl": Benchmark.scalar_precision_score(
                financial_document.total_incl, ground_truth.total_incl),
            "__pre__total_excl": Benchmark.scalar_precision_score(
                financial_document.total_excl, ground_truth.total_excl),
            "__pre__invoice_date": Benchmark.scalar_precision_score(
                financial_document.date, ground_truth.date),
            "__pre__invoice_number": Benchmark.scalar_precision_score(
                financial_document.invoice_number, ground_truth.invoice_number),
            "__pre__due_date": Benchmark.scalar_precision_score(
                financial_document.due_date, ground_truth.due_date),
            "__pre__total_tax": Benchmark.scalar_precision_score(
                financial_document.total_tax, ground_truth.total_tax)}

        if len(financial_document.taxes) == 0:
            precisions["__pre__taxes"] = None
        else:
            precisions["__pre__taxes"] = Tax.compare_arrays(financial_document.taxes, ground_truth.taxes)

        return precisions
