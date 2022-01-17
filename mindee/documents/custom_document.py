from mindee.documents import Document
from mindee.http import make_api_request


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
        self.fields = None
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
        self.fields = api_prediction.keys()
        for field in api_prediction:
            setattr(self, field, api_prediction[field])
            getattr(self, field)["page_n"] = page_n

    def __str__(self) -> str:
        """
        :return: (str) String representation of the document
        """
        custom_doc_str = "----- " + self.type + " -----\n"
        for field in self.fields:
            custom_doc_str += "%s: %s\n" % (
                field,
                "".join(
                    [
                        field_value["content"]
                        for field_value in getattr(self, field)["values"]
                    ]
                ),
            )
        custom_doc_str += "-----------------\n"
        return custom_doc_str

    @staticmethod
    def request(input_file, url, api_key):
        """
        Make request to invoices endpoint
        :param url: Endpoint URL
        :param input_file: Input object
        :param api_key: Endpoint API Key
        """
        return make_api_request(url, input_file, api_key)

    def _checklist(self):
        return {}
