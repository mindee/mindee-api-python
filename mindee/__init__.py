import json

from mindee.http import HTTPException
from mindee.inputs import Inputs
from mindee.documents import Document
from mindee.documents.car_plate import CarPlate
from mindee.documents.receipt import Receipt
from mindee.documents.financial_document import FinancialDocument
from mindee.documents.invoice import Invoice
from mindee.documents.passport import Passport
from mindee.benchmark import Benchmark


class Client(object):
    def __init__(
            self,
            expense_receipt_token=None,
            invoice_token=None,
            passport_token=None,
            license_plate_token=None,
            raise_on_error=True
    ):
        """
        :param expense_receipt_token: expense_receipt Mindee API token, see https://mindee.com
        :param invoice_token: invoice Mindee API token, see https://mindee.com
        :param passport_token: passport Mindee API token, see https://mindee.com
        :param license_plate_token: license_plate Mindee API token, see https://mindee.com
        :param raise_on_error: (bool, default True) raise an Exception on HTTP errors
        """
        assert type(raise_on_error) == bool
        self.raise_on_error = raise_on_error
        self.base_url = "https://api.mindee.net/products/"
        self.expense_receipt_token = expense_receipt_token
        self.invoice_token = invoice_token
        self.passport_token = passport_token
        self.license_plate_token = license_plate_token

    def parse_receipt(
            self,
            file,
            input_type="path",
            version="3",
            cut_pdf=True,
            include_words=False
    ):
        """
        :param include_words: Bool, extract all words into http_response
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        :param input_type: String in {'path', 'stream', 'base64'}
        :param file: Receipt filepath (allowed jpg, png, tiff, pdf)
        :param version: expense_receipt api version
        :return: Wrapped response with Receipts objects parsed
        """
        if not self.expense_receipt_token:
            raise Exception("Missing 'expense_receipt_token' arg in parse_receipt() function.")

        input_file = Inputs(file, input_type, cut_pdf=cut_pdf)

        response = Receipt.request(
            input_file,
            self.base_url,
            self.expense_receipt_token,
            version,
            include_words
        )

        return self._wrap_response(input_file, response, "receipt")

    def _wrap_response(
            self,
            input_file,
            response,
            document_type
    ):
        """
        :param input_file: Input object
        :param response: HTTP response
        :param document_type: Document class in {"receipt", "invoice", "financial_document", "passport", "license_plate"}
        :return: Full response object
        """
        dict_response = response.json()
        if response.status_code != 200 and self.raise_on_error:
            raise HTTPException(
                "Receipt API %s HTTP error: %s" % (response.status_code, json.dumps(dict_response)))
        elif response.status_code != 200:
            return Response(
                http_response=dict_response,
                pages=[],
                document=None,
                document_type=document_type
            )

        return Response.format_response(dict_response, document_type, input_file)

    def parse_passport(
            self,
            file,
            input_type="path",
            version="1",
            cut_pdf=True
    ):
        """
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        :param input_type: String in {'path', 'stream', 'base64'}
        :param file: Passport filepath (allowed jpg, png, pdf)
        :param version: passport api version
        :return: Wrapped response with passports objects parsed
        """
        if not self.passport_token:
            raise Exception("Missing 'passport_token' arg in parse_passport() function.")

        input_file = Inputs(file, input_type, cut_pdf=cut_pdf)

        response = Passport.request(
            input_file,
            self.base_url,
            self.passport_token,
            version
        )

        return self._wrap_response(input_file, response, "passport")

    def parse_license_plate(
            self,
            file,
            input_type="path",
            version="1",
            cut_pdf=True
    ):
        """
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        :param input_type: String in {'path', 'stream', 'base64'}
        :param file: CarPlate filepath (allowed jpg, png, pdf)
        :param version: license_plates api version
        :return: Wrapped response with CarPlates objects parsed
        """
        if not self.license_plate_token:
            raise Exception("Missing 'license_plate_token' arg in license_plate_token() function.")

        input_file = Inputs(file, input_type, cut_pdf=cut_pdf)

        response = CarPlate.request(
            input_file,
            self.base_url,
            self.license_plate_token,
            version
        )

        return self._wrap_response(input_file, response, "license_plate")

    def parse_invoice(
            self,
            file,
            input_type="path",
            version="2",
            cut_pdf=True,
            include_words=False
    ):
        """
        :param include_words: Bool, extract all words into http_response
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        :param input_type: String in {'path', 'stream', 'base64'}
        :param file: Invoice filepath (allowed jpg, png, pdf)
        :param version: invoices api version
        :return: Wrapped response with Invoices objects parsed
        """
        if not self.invoice_token:
            raise Exception("Missing 'invoice_token' arg in parse_invoice() function.")

        input_file = Inputs(file, input_type, cut_pdf=cut_pdf)

        response = Invoice.request(
            input_file,
            self.base_url,
            self.invoice_token,
            version,
            include_words
        )

        return self._wrap_response(input_file, response, "invoice")

    def parse_financial_document(
            self,
            file,
            input_type="path",
            cut_pdf=True,
            include_words=False
    ):
        """
        :param include_words: Bool, extract all words into http_response
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        :param input_type: String in {'path', 'stream', 'base64'}
        :param file: Invoice or Receipt filepath (allowed jpg, png, pdf)
        :return: Wrapped response with FinancialDocument objects parsed
        """
        if not self.invoice_token or not self.expense_receipt_token:
            raise Exception("parse_invoice() function must include 'invoice_token' and 'expense_receipt_token' args.")

        input_file = Inputs(file, input_type, cut_pdf=cut_pdf)

        response = FinancialDocument.request(
            input_file,
            self.base_url,
            self.expense_receipt_token,
            self.invoice_token,
            include_words
        )

        return self._wrap_response(input_file, response, "financial_document")


class Response(object):
    def __init__(
            self,
            http_response=None,
            pages=None,
            document=None,
            document_type=None
    ):
        """
        :param http_response: HTTP response object
        :param pages: List of document objects
        :param document: reconstructed object from all pages
        :param document_type: Document class in {"receipt", "invoice", "financial_document", "passport", "license_plate"}
        """
        self.http_response = http_response
        self.document_type = document_type
        if document_type == "receipt":
            self.receipt = document
            self.receipts = pages
        if document_type == "invoice":
            self.invoice = document
            self.invoices = pages
        if document_type == "financial_document":
            self.financial_document = document
            self.financial_documents = pages
        if document_type == "passport":
            self.passport = document
            self.passports = pages
        if document_type == "license_plate":
            self.license_plate = document
            self.license_plates = pages

    def dump(self, path):
        """
        :param path: file path for storing the response object
        :return: (void) save the json response
        """
        with open(path, "w") as fp:
            json.dump(self.http_response, fp)

    @staticmethod
    def load(json_path):
        """
        :param json_path: file of the json reponse to restore
        :return: Full response object loaded from json file
        """
        try:
            with open(json_path) as fp:
                json_response = json.load(fp)

            file_input = Inputs.load(
                json_response["input_type"],
                json_response["filename"],
                json_response["filepath"],
                json_response["file_extension"]
            )
            response = Response.format_response(
                json_response,
                document_type=json_response["document_type"],
                input_file=file_input
            )
            return response
        except:
            raise Exception("Unable to load file.")

    @staticmethod
    def format_response(json_response, document_type, input_file):
        """
        :param input_file: Input object
        :param json_response: json response from HTTP call
        :param document_type: Document class in {"receipt", "invoice", "financial_document", "passport", "license_plate"}
        :return: Full Response object
        """
        json_response["document_type"] = document_type
        json_response["input_type"] = input_file.input_type
        json_response["filename"] = input_file.filename
        json_response["filepath"] = input_file.filepath
        json_response["file_extension"] = input_file.file_extension
        pages = []
        for page_n, page_prediction in enumerate(json_response["predictions"]):
            if document_type == "receipt":
                pages.append(
                    Receipt(
                        api_prediction=page_prediction,
                        input_file=input_file,
                        page_n=page_n
                    )
                )
            elif document_type == "invoice":
                pages.append(
                    Invoice(
                        api_prediction=page_prediction,
                        input_file=input_file,
                        page_n=page_n
                    )
                )
            elif document_type == "financial_document":
                pages.append(
                    FinancialDocument(
                        api_prediction=page_prediction,
                        input_file=input_file,
                        page_n=page_n
                    )
                )
            elif document_type == "passport":
                pages.append(
                    Passport(
                        api_prediction=page_prediction,
                        input_file=input_file,
                        page_n=page_n
                    )
                )
            elif document_type == "license_plate":
                pages.append(
                    CarPlate(
                        api_prediction=page_prediction,
                        input_file=input_file,
                        page_n=page_n
                    )
                )
            else:
                raise Exception("Document type not supported.")

        document = Document.merge_pages(pages)

        return Response(
            http_response=json_response,
            pages=pages,
            document=document,
            document_type=document_type
        )
