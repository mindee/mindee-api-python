from typing import List, Type, Optional

# from mindee.inputs import InputDocument
from mindee.http import Endpoint


class Document:
    type: str
    checklist: dict = {}
    filepath: Optional[str] = None
    filename: Optional[str] = None
    file_extension: Optional[str] = None

    def __init__(
        self,
        input_file,
        document_type: str,
        api_prediction,
        page_n: Optional[int] = None,
    ):
        if input_file:
            self.filepath = input_file.filepath
            self.filename = input_file.filename
            self.file_extension = input_file.file_extension

        self.type = document_type

        self.build_from_api_prediction(api_prediction, page_n=page_n)
        self._checklist()
        self._reconstruct()

    @staticmethod
    def request(endpoints: List[Endpoint], input_file, include_words: bool = False):
        """Make request to the product endpoint"""
        raise NotImplementedError()

    def build_from_api_prediction(self, api_prediction: dict, page_n):
        """Build the document from an API response JSON"""
        raise NotImplementedError()

    def _checklist(self, *args):
        raise NotImplementedError()

    def _reconstruct(self, *args):
        pass

    def all_checks(self):
        """Return all checks"""
        return all(self.checklist)


TypeDocument = Type[Document]
