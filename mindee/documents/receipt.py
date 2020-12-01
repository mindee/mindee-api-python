from mindee.benchmark import Benchmark
from mindee.documents import Document
from mindee.fields import Field
from mindee.fields.date import Date
from mindee.fields.amount import Amount
from mindee.fields.locale import Locale
from mindee.fields.orientation import Orientation
from mindee.fields.tax import Tax
from mindee.http import request
import os


class Receipt(Document):
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
            page_n=0
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
        self.type = "Receipt"
        self.locale = None
        self.total_incl = None
        self.date = None
        self.category = None
        self.merchant_name = None
        self.time = None
        self.taxes = []
        self.orientation = None
        self.total_tax = None
        self.total_excl = None

        if api_prediction is not None:
            self.build_from_api_prediction(api_prediction, page_n=page_n)
        else:
            self.locale = Locale({"value": locale}, value_key="value", page_n=page_n)
            self.total_incl = Amount({"value": total_incl}, value_key="value", page_n=page_n)
            self.date = Date({"value": date}, value_key="value", page_n=page_n)
            self.category = Field({"value": category}, value_key="value", page_n=page_n)
            self.merchant_name = Field({"value": merchant_name}, value_key="value", page_n=page_n)
            self.time = Field({"value": time}, value_key="value", page_n=page_n)
            if taxes is not None:
                self.taxes = [
                    Tax({"value": t[0], "rate": t[1]}, page_n=page_n, value_key="value", rate_key="rate")
                    for t in taxes]
            self.orientation = Orientation({"value": orientation}, value_key="value", page_n=page_n)
            self.total_tax = Amount({"value": total_tax}, value_key="value", page_n=page_n)
            self.total_excl = Amount({"value": total_excl}, value_key="value", page_n=page_n)

        # Invoke Document constructor
        super(Receipt, self).__init__(input_file)

        # Run checks
        self._checklist()

        # Reconstruct extra fields
        self._reconstruct()

    def __str__(self):
        return "-----Receipt data-----\n" \
               "Filename: %s\n" \
               "Total amount: %s \n" \
               "Date: %s\n" \
               "Category: %s\n" \
               "Time: %s\n" \
               "Merchant name: %s\n" \
               "Taxes: %s\n" \
               "Total taxes: %s\n" \
               "----------------------" % \
               (
                   self.filename,
                   self.total_incl.value,
                   self.date.value,
                   self.category.value,
                   self.time.value,
                   self.merchant_name.value,
                   " - ".join([str(t) for t in self.taxes]),
                   self.total_tax.value
               )

    def build_from_api_prediction(self, api_prediction, page_n=0):
        """
        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number for multi pages pdf input
        :return: (void) set the object attributes with api prediction values
        """
        self.locale = Locale(api_prediction["locale"], page_n=page_n)
        self.total_incl = Amount(api_prediction["total_incl"], value_key="value", page_n=page_n)
        self.date = Date(api_prediction["date"], value_key="value", page_n=page_n)
        self.category = Field(api_prediction["category"], page_n=page_n)
        self.merchant_name = Field(api_prediction["supplier"], value_key="value", page_n=page_n)
        self.time = Field(api_prediction["time"], value_key="value", page_n=page_n)
        self.taxes = [
            Tax(tax_prediction, page_n=page_n, value_key="value", rate_key="rate", code_key="code")
            for tax_prediction in api_prediction["taxes"]]
        self.orientation = Orientation(api_prediction["orientation"], page_n=page_n)
        self.total_tax = Amount({"value": None, "probability": 0.}, value_key="value", page_n=page_n)
        self.total_excl = Amount({"value": None, "probability": 0.}, value_key="value", page_n=page_n)

    @staticmethod
    def compare(receipt=None, ground_truth=None):
        """
        :param receipt: Receipt object to compare
        :param ground_truth: Ground truth Receipt object
        :return: Accuracy and precisions metrics
        """
        assert receipt is not None
        assert ground_truth is not None
        assert isinstance(receipt, Receipt)
        assert isinstance(ground_truth, Receipt)

        metrics = {}

        # Compute Accuracy metrics
        metrics.update(Receipt.compute_accuracy(receipt, ground_truth))

        # Compute precision metrics
        metrics.update(Receipt.compute_precision(receipt, ground_truth))

        return metrics

    @staticmethod
    def request(
            input_file,
            base_url,
            expense_receipt_token=None,
            version="3",
            include_words=False
    ):
        """
        Make request to expense_receipts endpoint
        :param input_file: Input object
        :param base_url: API base URL
        :param expense_receipt_token: Expense_receipts API token
        :param include_words: Include Mindee vision words in http_response
        :param version: API version
        """
        url = os.path.join(base_url, "expense_receipts", "v" + version, "predict")
        return request(url, input_file, expense_receipt_token, include_words)

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
    def __taxes_match_total(self):
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

        if self.total_incl.value * (1 - eps) - 0.02 <= reconstructed_total <= self.total_incl.value * (
                1 + eps) + 0.02:
            for tax in self.taxes:
                tax.probability = 1
            self.total_tax.probability = 1.
            self.total_incl.probability = 1.
            return True
        else:
            return False

    # Reconstruct
    def __reconstruct_total_excl_from_tcc_and_taxes(self):
        """
        Set self.total_excl with Amount object
        The total_excl Amount value is the difference between total_incl and sum of taxes
        The total_excl Amount probability is the product of self.taxes probabilities multiplied by total_incl probability
        """
        if len(self.taxes) and self.total_incl.value is not None:
            total_excl = {
                "value": self.total_incl.value - Field.array_sum(self.taxes),
                "probability": Field.array_probability(self.taxes) * self.total_incl.probability
            }
            self.total_excl = Amount(total_excl, value_key="value", reconstructed=True)

    def __reconstruct_total_tax(self):
        """
        Set self.total_tax with Amount object
        The total_tax Amount value is the sum of all self.taxes value
        The total_tax Amount probability is the product of self.taxes probabilities
        """
        if len(self.taxes) and self.total_tax.value is None:
            total_tax = {
                "value": sum([tax.value if tax.value is not None else 0 for tax in self.taxes]),
                "probability": Field.array_probability(self.taxes)
            }
            if total_tax["value"] > 0:
                self.total_tax = Amount(total_tax, value_key="value", reconstructed=True)

    @staticmethod
    def compute_accuracy(receipt, ground_truth):
        """
        :param receipt: Receipt object to compare
        :param ground_truth: Ground truth Receipt object
        :return: Accuracy metrics
        """
        return {
            "__acc__total_incl": ground_truth.total_incl == receipt.total_incl,
            "__acc__total_excl": ground_truth.total_excl == receipt.total_excl,
            "__acc__receipt_date": ground_truth.date == receipt.date,
            "__acc__total_tax": ground_truth.total_tax == receipt.total_tax,
            "__acc__taxes": Tax.compare_arrays(receipt.taxes, ground_truth.taxes),
        }

    @staticmethod
    def compute_precision(receipt, ground_truth):
        """
        :param receipt: Receipt object to compare
        :param ground_truth: Ground truth Receipt object
        :return: Precision metrics
        """
        precisions = {
            "__pre__total_incl": Benchmark.scalar_precision_score(
                receipt.total_incl, ground_truth.total_incl),
            "__pre__total_excl": Benchmark.scalar_precision_score(
                receipt.total_excl, ground_truth.total_excl),
            "__pre__receipt_date": Benchmark.scalar_precision_score(
                receipt.date, ground_truth.date),
            "__pre__total_tax": Benchmark.scalar_precision_score(
                receipt.total_tax, ground_truth.total_tax)}

        if len(receipt.taxes) == 0:
            precisions["__pre__taxes"] = None
        else:
            precisions["__pre__taxes"] = Tax.compare_arrays(receipt.taxes, ground_truth.taxes)

        return precisions
