from typing import List

# from mindee.inputs import InputDocument
from mindee.http import Endpoint


class Document:
    type: str

    def __init__(
        self, input_file, document_type: str, api_prediction, page_n=0
    ):  # pylint: disable=unused-argument
        self.filepath = None
        self.filename = None
        self.file_extension = None

        if input_file is not None:
            self.filepath = input_file.filepath
            self.filename = input_file.filename
            self.file_extension = input_file.file_extension

        self.type = document_type
        self.checklist: dict = {}

    @staticmethod
    def request(endpoints: List[Endpoint], input_file, include_words: bool = False):
        """Make request to the product endpoint"""
        raise NotImplementedError()

    def _checklist(self, *args):
        raise NotImplementedError()

    def _reconstruct(self, *args):
        pass

    def all_checks(self):
        """Return all checks"""
        return all(self.checklist)
