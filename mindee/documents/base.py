import datetime
from typing import List, Optional, Type

# from mindee.inputs import InputDocument
from mindee.http import Endpoint


def serialize_for_json(obj):
    """
    Custom serializer for Document objects.

    Use as the `default` argument of the `json.dump` functions.
    """
    if isinstance(obj, datetime.date):
        return obj.__str__()
    return vars(obj)


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
    def request(
        endpoints: List[Endpoint],
        input_file,
        include_words: bool = False,
        close_file: bool = True,
    ):
        """
        Make request to prediction endpoint.

        :param input_file: Input object
        :param endpoints: Endpoints config
        :param include_words: Include Mindee vision words in http_response
        :param close_file: Whether to `close()` the file after parsing it.
        """
        return endpoints[0].predict_request(input_file, include_words, close_file)

    def build_from_api_prediction(self, api_prediction: dict, page_n):
        """Build the document from an API response JSON."""
        raise NotImplementedError()

    def _checklist(self) -> None:
        raise NotImplementedError()

    def _reconstruct(self) -> None:
        pass

    def all_checks(self) -> bool:
        """Return all checks."""
        return all(self.checklist)


TypeDocument = Type[Document]
