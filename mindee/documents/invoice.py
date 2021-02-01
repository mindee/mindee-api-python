from mindee.documents import Document
from mindee.fields import Field
from mindee.fields.date import Date
from mindee.fields.amount import Amount
from mindee.fields.locale import Locale
from mindee.fields.orientation import Orientation
from mindee.fields.payment_details import PaymentDetails
from mindee.fields.tax import Tax
from mindee.http import request
from mindee.benchmark import Benchmark
import os


class Invoice(Document):
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
            vat_number=None,
            orientation=None,
            total_tax=None,
            page_n=0
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
        :param vat_number: vat_number value for creating Invoice object from scratch
        :param orientation: orientation value for creating Invoice object from scratch
        :param total_tax: total_tax value for creating Invoice object from scratch
        :param page_n: Page number for multi pages pdf input
        """
        self.type = "Invoice"
        self.locale = None
        self.total_incl = None
        self.total_excl = None
        self.invoice_date = None
        self.invoice_number = None
        self.due_date = None
        self.taxes = []
        self.supplier = None
        self.payment_details = None
        self.company_number = None
        self.orientation = None
        self.total_tax = None

        if api_prediction is not None:
            self.build_from_api_prediction(api_prediction, page_n=page_n)
        else:
            self.locale = Locale({"value": locale}, value_key="value", page_n=page_n)
            self.total_incl = Amount({"value": total_incl}, value_key="value", page_n=page_n)
            self.date = Date({"value": invoice_date}, value_key="value", page_n=page_n)
            self.invoice_date = Date({"value": invoice_date}, value_key="value", page_n=page_n)
            self.due_date = Date({"value": due_date}, value_key="value", page_n=page_n)
            self.supplier = Field({"value": supplier}, value_key="value", page_n=page_n)
            if taxes is not None:
                self.taxes = [
                    Tax({"value": t[0], "rate": t[1]}, page_n=page_n, value_key="value", rate_key="rate")
                    for t in taxes]
            self.orientation = Orientation({"value": orientation}, value_key="value", page_n=page_n)
            self.total_tax = Amount({"value": total_tax}, value_key="value", page_n=page_n)
            self.total_excl = Amount({"value": total_excl}, value_key="value", page_n=page_n)
            self.invoice_number = Field({"value": invoice_number}, value_key="value", page_n=page_n)
            self.payment_details = Field({"value": payment_details}, value_key="value", page_n=page_n)
            self.company_number = Field({"value": company_number}, value_key="value", page_n=page_n)

        # Invoke Document constructor
        super(Invoice, self).__init__(input_file)

        # Run checks
        self._checklist()

        # Reconstruct extra fields
        self._reconstruct()

    def build_from_api_prediction(self, api_prediction, page_n=0):
        """
        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number for multi pages pdf input
        :return: (void) set the object attributes with api prediction values
        """
        self.company_number = [
            Field(company_reg, extra_fields={"type"}, page_n=page_n) for company_reg in
            api_prediction["company_registration"]
        ]
        self.invoice_date = Date(api_prediction["date"], value_key="value", page_n=page_n)
        self.due_date = Date(api_prediction["due_date"], value_key="value", page_n=page_n)
        self.invoice_number = Field(api_prediction["invoice_number"], page_n=page_n)
        self.locale = Locale(api_prediction["locale"], value_key="language", page_n=page_n)
        self.orientation = Orientation(api_prediction["orientation"], page_n=page_n)
        self.supplier = Field(api_prediction["supplier"], page_n=page_n)
        self.taxes = [
            Tax(tax_prediction, page_n=page_n, value_key="value") for tax_prediction in api_prediction["taxes"]
        ]
        self.payment_details = [
            PaymentDetails(
                payment_detail,
                page_n=page_n
            ) for payment_detail in api_prediction["payment_details"]
        ]
        self.total_incl = Amount(api_prediction["total_incl"], value_key="value", page_n=page_n)
        self.total_excl = Amount(api_prediction["total_excl"], value_key="value", page_n=page_n)
        self.total_tax = Amount({"value": None, "probability": 0.}, value_key="value", page_n=page_n)

    def __str__(self):
        return "-----Invoice data-----\n" \
               "Filename: %s \n" \
               "Invoice number: %s \n" \
               "Total amount including taxes: %s \n" \
               "Total amount excluding taxes: %s \n" \
               "Invoice date: %s\n" \
               "Supplier name: %s\n" \
               "Taxes: %s\n" \
               "Total taxes: %s\n" \
               "----------------------" % \
               (
                   self.filename,
                   self.invoice_number.value,
                   self.total_incl.value,
                   self.total_excl.value,
                   self.invoice_date.value,
                   self.supplier.value,
                   ",".join([str(t.value) + " " + str(t.rate) + "%" for t in self.taxes]),
                   self.total_tax.value
               )

    @staticmethod
    def compare(invoice=None, ground_truth=None):
        """
        :param invoice: Invoice object to compare
        :param ground_truth: Ground truth Invoice object
        :return: Accuracy and precisions metrics
        """
        assert invoice is not None
        assert ground_truth is not None
        assert isinstance(invoice, Invoice)
        assert isinstance(ground_truth, Invoice)

        metrics = {}

        # Compute Accuracy metrics
        metrics.update(Invoice.compute_accuracy(invoice, ground_truth))

        # Compute precision metrics
        metrics.update(Invoice.compute_precision(invoice, ground_truth))

        return metrics

    @staticmethod
    def request(
            input_file,
            base_url,
            invoice_token=None,
            version="2",
            include_words=False
    ):
        """
        Make request to invoices endpoint
        :param input_file: Input object
        :param base_url: API base URL
        :param invoice_token: Invoices API token
        :param include_words: Include Mindee vision words in http_response
        :param version: API version
        """
        url = os.path.join(base_url, "invoices", "v" + version, "predict")
        return request(url, input_file, invoice_token, include_words)

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
            "taxes_plus_total_excl_match_total_incl": self.__taxes_plus_total_excl_match_total_incl()
        }

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
        if self.total_excl.value * (1 - eps) - 0.02 <= reconstructed_total <= self.total_excl.value * (
                1 + eps) + 0.02:
            for tax in self.taxes:
                tax.probability = 1
            self.total_tax.probability = 1.
            self.total_excl.probability = 1.
            return True
        else:
            return False

    def __taxes_plus_total_excl_match_total_incl(self):
        """
        Check invoice rule of matching : sum(taxes) + total_excluding_taxes = total_including_taxes
        :return: True if rule matches, False otherwise
        """
        # Check total_tax, total excl and total incl exist
        if self.total_excl.value is None or len(self.taxes) == 0 or self.total_incl.value is None:
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
        if self.total_incl.value - 0.01 <= reconstructed_total <= self.total_incl.value + 0.01:
            for tax in self.taxes:
                tax.probability = 1
            self.total_tax.probability = 1.
            self.total_excl.probability = 1.
            self.total_incl.probability = 1.
            return True
        else:
            return False

    # Reconstruct
    def __reconstruct_total_incl_from_taxes_plus_excl(self):
        """
        Set self.total_incl with Amount object
        The total_incl Amount value is the sum of total_excl and sum of taxes
        The total_incl Amount probability is the product of self.taxes probabilities multiplied by total_excl probability
        """
        # Check total_tax, total excl exist and total incl is not set
        if self.total_excl.value is None or len(self.taxes) == 0 or self.total_incl.value is not None:
            pass
        else:
            total_incl = {
                "value": sum([tax.value if tax.value is not None else 0 for tax in self.taxes]) + self.total_excl.value,
                "probability": Field.array_probability(self.taxes) * self.total_excl.probability
            }
            self.total_incl = Amount(total_incl, value_key="value", reconstructed=True)

    def __reconstruct_total_excl_from_tcc_and_taxes(self):
        """
        Set self.total_excl with Amount object
        The total_excl Amount value is the difference between total_incl and sum of taxes
        The total_excl Amount probability is the product of self.taxes probabilities multiplied by total_incl probability
        """
        # Check total_tax, total excl and total incl exist
        if self.total_incl.value is None or len(self.taxes) == 0 or self.total_excl.value is not None:
            pass
        else:
            total_excl = {
                "value": self.total_incl.value - sum([tax.value if tax.value is not None else 0 for tax in self.taxes]),
                "probability": Field.array_probability(self.taxes) * self.total_incl.probability
            }
            self.total_excl = Amount(total_excl, value_key="value", reconstructed=True)

    def __reconstruct_total_tax_from_tax_lines(self):
        """
        Set self.total_tax with Amount object
        The total_tax Amount value is the sum of all self.taxes value
        The total_tax Amount probability is the product of self.taxes probabilities
        """
        if len(self.taxes):
            total_tax = {
                "value": sum([tax.value if tax.value is not None else 0 for tax in self.taxes]),
                "probability": Field.array_probability(self.taxes)
            }
            if total_tax["value"] > 0:
                self.total_tax = Amount(total_tax, value_key="value", reconstructed=True)

    def __reconstruct_total_tax_from_incl_and_excl(self):
        """
        Set self.total_tax with Amount object
        Check if the total tax was already set
        If not, set thta total tax amount to the diff of incl and excl
        """
        if self.total_tax.value is not None or\
                self.total_excl.value is None or\
                self.total_incl.value is None:
                pass
        else:

            total_tax = {
                "value": self.total_incl.value - self.total_excl.value,
                "probability": self.total_incl.probability * self.total_excl.probability
            }
            if total_tax["value"] >= 0:
                self.total_tax = Amount(total_tax, value_key="value", reconstructed=True)

    @staticmethod
    def compute_accuracy(invoice, ground_truth):
        """
        :param invoice: Invoice object to compare
        :param ground_truth: Ground truth Invoice object
        :return: Accuracy metrics
        """
        return {
            "__acc__total_incl": ground_truth.total_incl == invoice.total_incl,
            "__acc__total_excl": ground_truth.total_excl == invoice.total_excl,
            "__acc__invoice_date": ground_truth.invoice_date == invoice.invoice_date,
            "__acc__invoice_number": ground_truth.invoice_number == invoice.invoice_number,
            "__acc__due_date": ground_truth.due_date == invoice.due_date,
            "__acc__total_tax": ground_truth.total_tax == invoice.total_tax,
            "__acc__taxes": Tax.compare_arrays(invoice.taxes, ground_truth.taxes),
        }

    @staticmethod
    def compute_precision(invoice, ground_truth):
        """
        :param invoice: Invoice object to compare
        :param ground_truth: Ground truth Invoice object
        :return: Precision metrics
        """
        precisions = {
            "__pre__total_incl": Benchmark.scalar_precision_score(
                invoice.total_incl, ground_truth.total_incl),
            "__pre__total_excl": Benchmark.scalar_precision_score(
                invoice.total_excl, ground_truth.total_excl),
            "__pre__invoice_date": Benchmark.scalar_precision_score(
                invoice.invoice_date, ground_truth.invoice_date),
            "__pre__invoice_number": Benchmark.scalar_precision_score(
                invoice.invoice_number, ground_truth.invoice_number),
            "__pre__due_date": Benchmark.scalar_precision_score(
                invoice.due_date, ground_truth.due_date),
            "__pre__total_tax": Benchmark.scalar_precision_score(
                invoice.total_tax, ground_truth.total_tax)}

        if len(invoice.taxes) == 0:
            precisions["__pre__taxes"] = None
        else:
            precisions["__pre__taxes"] = Tax.compare_arrays(invoice.taxes, ground_truth.taxes)

        return precisions
