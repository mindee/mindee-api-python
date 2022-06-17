import datetime
from typing import Any, Dict, List, Optional, Type

from mindee.endpoints import Endpoint
from mindee.inputs import InputDocument

TypeApiPrediction = Dict[str, Any]


def serialize_for_json(obj: Any) -> Any:
    """
    Custom serializer for Document objects.

    Use as the `default` argument of the `json.dump` functions.
    """
    if isinstance(obj, datetime.date):
        return obj.__str__()
    return vars(obj)


class Document:
    type: str
    """Document type"""
    checklist: dict = {}
    """Validation checks for the document"""
    filepath: Optional[str] = None
    """Path of the input document"""
    filename: Optional[str] = None
    """Name of the input document"""
    file_extension: Optional[str] = None
    """File extension of the input document"""

    def __init__(
        self,
        input_file: InputDocument,
        document_type: str,
        api_prediction: TypeApiPrediction,
        page_n: Optional[int] = None,
    ):
        if input_file:
            self.filepath = input_file.filepath
            self.filename = input_file.filename
            self.file_extension = input_file.file_mimetype

        self.type = document_type

        self._build_from_api_prediction(api_prediction, page_n=page_n)
        self._checklist()
        self._reconstruct()

    @staticmethod
    def request(
        endpoints: List[Endpoint],
        input_file: InputDocument,
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

    def _build_from_api_prediction(
        self, api_prediction: TypeApiPrediction, page_n: Optional[int] = None
    ) -> None:
        """Build the document from an API response JSON."""
        raise NotImplementedError()

    def _checklist(self) -> None:
        raise NotImplementedError()

    def _reconstruct(self) -> None:
        pass

    def all_checks(self) -> bool:
        """Return status of all checks."""
        return all(self.checklist)


TypeDocument = Type[Document]
