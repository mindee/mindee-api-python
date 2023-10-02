from typing import Dict, List, Optional, TypeVar

from mindee.http.endpoints import Endpoint
from mindee.input.sources import InputSource
from mindee.parsing.common.api_response import StringDict
from mindee.parsing.common.prediction import Prediction
from mindee.parsing.standard.position import PositionField


class Inference:
    """Base Inference class for all predictions."""

    type: Optional[str]
    """Document type"""
    checklist: dict
    """Validation checks for the document"""
    filepath: Optional[str] = None
    """Path of the input document"""
    filename: Optional[str] = None
    """Name of the input document"""
    file_extension: Optional[str] = None
    """Page orientation"""
    cropper: List[PositionField]
    """Cropper results"""
    product_name: str
    """Name of the product as sent by the API."""
    product_version: str
    """Version of the product as sent by the API."""
    endpoint_name: Optional[str]
    """Name of the endpoint for OTS APIs"""
    endpoint_version: Optional[str]
    """Version of the endpoint for OTS APIs"""
    prediction: Prediction
    """A document's top-level Prediction."""
    pages: List[Prediction]
    """A document's pages."""
    is_rotation_applied: bool
    """Whether the document has had any rotation applied to it."""

    def __init__(
        self,
        raw_prediction: StringDict,
    ):
        self.is_rotation_applied = (
            "is_rotation_applied" in raw_prediction
            and raw_prediction["is_rotation_applied"]
        )
        if "product" in raw_prediction and raw_prediction["product"]:
            if "name" in raw_prediction["product"]:
                self.product_name = raw_prediction["product"]["name"]
            if "version" in raw_prediction["product"]:
                self.product_version = raw_prediction["product"]["version"]

    @staticmethod
    def request(
        endpoints: List[Endpoint],
        input_source: InputSource,
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

    def _build_from_raw_json(
        self, raw_json: StringDict, page_id: Optional[int] = None
    ) -> None:
        """Build the document from an API response JSON."""
        raise NotImplementedError()

    def __str__(self) -> str:
        return (
            f"Inference"
            f"#########"
            f":Product: {self.product_name} v{self.product_version}"
        )

    def get_endpoint_info(self) -> Dict[str, str]:
        if self.endpoint_name and self.endpoint_version:
            return {"name": self.endpoint_name, "version": self.endpoint_version}
        raise TypeError("Can't get endpoint information for {self.__name__}")


TypeInference = TypeVar("TypeInference", bound=Inference)
