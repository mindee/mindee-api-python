from mindee.documents import Document
from mindee.http import make_api_request, make_predict_url


class CustomDocument(Document):
    def __init__(
        self,
        document_type="",
        api_prediction=None,
        input_file=None,
        page_n=0,
    ):
        """
        :param document_type: Document type
        :param api_prediction: Raw prediction from HTTP response
        :param input_file: Input object
        :param page_n: Page number for multi pages pdf input
        """
        self.type = document_type
        self.build_from_api_prediction(api_prediction, page_n=page_n)
        # Invoke Document constructor
        super(CustomDocument, self).__init__(input_file)

    def build_from_api_prediction(self, api_prediction, page_n=0):
        """
        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number for multi pages pdf input
        :return: (void) set the object attributes with api prediction values
        """
        for field in api_prediction:
            setattr(self, field, api_prediction[field])

    def __str__(self):
        # TODO: loop on fields and print them
        return "----- " + self.type + " -----"

    @staticmethod
    def request(input_file, url, api_key):
        """
        Make request to invoices endpoint
        :param url: Endpoint URL
        :param input_file: Input object
        :param api_key: Endpoint API Key
        """
        return make_api_request(url, input_file, api_key)
