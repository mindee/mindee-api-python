from typing import Dict

from mindee.documents.base import Document


class CustomDocument(Document):
    fields: Dict[str, dict] = {}

    def __init__(
        self,
        document_type: str,
        api_prediction=None,
        input_file=None,
        page_n: int = 0,
    ):
        """
        Custom document object.

        :param document_type: Document type
        :param api_prediction: Raw prediction from HTTP response
        :param input_file: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_file=input_file,
            document_type=document_type,
            api_prediction=api_prediction,
            page_n=page_n,
        )

    def build_from_api_prediction(self, api_prediction, page_n: int = 0):
        """
        Build the document from an API response JSON.

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
        custom_doc_str = f"----- {self.type} -----\n"
        for name, info in self.fields.items():
            custom_doc_str += "%s: %s\n" % (
                name,
                "".join([value["content"] for value in info["values"]]),
            )
        custom_doc_str += "-----------------\n"
        return custom_doc_str

    def _checklist(self) -> None:
        pass
