from typing import Dict
from mindee.documents.base import Document
from mindee.http import make_predict_url, make_api_request


class CustomDocument(Document):
    fields: Dict[str, dict] = {}

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
        super().__init__(input_file)

    def build_from_api_prediction(self, api_prediction, page_n: int = 0):
        """
        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number for multi pages pdf input
        :return: (void) set the object attributes with api prediction values
        """
        for field_name in api_prediction:
            field = api_prediction[field_name]
            field["page_n"] = page_n
            self.fields[field_name] = field
            setattr(self, field_name, field)

    def __str__(self) -> str:
        """
        :return: (str) String representation of the document
        """
        custom_doc_str = f"----- {self.type} -----\n"
        for name, info in self.fields.items():
            custom_doc_str += "%s: %s\n" % (
                name,
                "".join([value["content"] for value in info["values"]]),
            )
        custom_doc_str += "-----------------\n"
        return custom_doc_str

    @staticmethod
    def request(input_file, document_type, username, api_key, version):
        """
        Make request to invoices endpoint
        :param input_file: Input object
        :param document_type: Document type
        :param username: API username
        :param api_key: Endpoint API Key
        :param version: Interface version
        """
        url = make_predict_url(document_type, version, username)
        return make_api_request(url, input_file, api_key)

    def _checklist(self):
        return {}
