import datetime
import re
from typing import Any, Dict, List, Optional, TypeVar, Union

from mindee.endpoints import Endpoint
from mindee.fields.orientation import OrientationField
from mindee.fields.position import PositionField
from mindee.input.sources import LocalInputSource, UrlInputSource

TypeApiPrediction = Dict[str, Any]


def serialize_for_json(obj: Any) -> Any:
    """
    Custom serializer for Document objects.

    Use as the `default` argument of the `json.dump` functions.
    """
    if isinstance(obj, datetime.date):
        return str(obj)
    return vars(obj)


def clean_out_string(out_string: str) -> str:
    """Clean up the string representation."""
    regexp = re.compile(r" \n")
    return regexp.sub("\n", out_string)


class Document:
    """Base class for all predictions."""

    type: Optional[str]
    """Document type"""
    checklist: dict
    """Validation checks for the document"""
    filepath: Optional[str] = None
    """Path of the input document"""
    filename: Optional[str] = None
    """Name of the input document"""
    file_extension: Optional[str] = None
    """File extension of the input document"""
    # orientation is only present on page-level, not document-level
    orientation: Optional[OrientationField] = None
    """Page orientation"""
    cropper: List[PositionField]
    """Cropper results"""

    def __init__(
        self,
        input_source: Optional[Union[LocalInputSource, UrlInputSource]],
        document_type: Optional[str],
        api_prediction: TypeApiPrediction,
        page_n: Optional[int] = None,
    ):
        if input_source:
            if isinstance(input_source, UrlInputSource):
                self.filename = input_source.url
            else:
                self.filepath = input_source.filepath
                self.filename = input_source.filename
                self.file_extension = input_source.file_mimetype
        self.checklist = {}
        self.type = document_type

        if page_n is not None:
            self._set_extras(api_prediction["extras"])
            self.orientation = OrientationField(
                api_prediction["orientation"], page_n=page_n
            )

    @staticmethod
    def request(
        endpoints: List[Endpoint],
        input_source: Union[LocalInputSource, UrlInputSource],
        include_words: bool = False,
        close_file: bool = True,
        cropper: bool = False,
    ):
        """
        Make request to prediction endpoint.

        :param input_source: Input object
        :param endpoints: Endpoints config
        :param include_words: Include Mindee vision words in http_response
        :param close_file: Whether to `close()` the file after parsing it.
        :param cropper: Including Mindee cropper results.
        """
        return endpoints[0].predict_req_post(
            input_source, include_words, close_file, cropper=cropper
        )

    def _set_extras(self, extras: TypeApiPrediction):
        self.cropper = []
        try:
            for crop in extras["cropper"]["cropping"]:
                self.cropper.append(PositionField(crop))
        except KeyError:
            pass

    def _build_from_api_prediction(
        self, api_prediction: TypeApiPrediction, page_n: Optional[int] = None
    ) -> None:
        """Build the document from an API response JSON."""
        raise NotImplementedError()

    def _checklist(self) -> None:
        pass

    def _reconstruct(self) -> None:
        pass

    def all_checks(self) -> bool:
        """Return status of all checks."""
        return all(self.checklist)


TypeDocument = TypeVar("TypeDocument", bound=Document)
