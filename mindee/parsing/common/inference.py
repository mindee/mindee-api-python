from typing import Dict, Generic, List, Optional, TypeVar

from mindee.parsing.common.api_response import StringDict
from mindee.parsing.common.page import TypePage
from mindee.parsing.common.prediction import TypePrediction


class Inference(Generic[TypePrediction, TypePage]):
    """Base Inference class for all predictions."""

    product_name: str
    """Name of the product as sent by the API."""
    product_version: str
    """Version of the product as sent by the API."""
    endpoint_name: Optional[str]
    """Name of the endpoint for OTS APIs"""
    endpoint_version: Optional[str]
    """Version of the endpoint for OTS APIs"""
    prediction: TypePrediction
    """A document's top-level Prediction."""
    pages: List[TypePage]
    """A document's pages."""
    is_rotation_applied: Optional[bool]
    """Whether the document has had any rotation applied to it."""

    def __init__(
        self,
        raw_prediction: StringDict,
    ):
        self.is_rotation_applied = None
        if "is_rotation_applied" in raw_prediction:
            self.is_rotation_applied = raw_prediction["is_rotation_applied"]
        if "product" in raw_prediction and raw_prediction["product"]:
            if "name" in raw_prediction["product"]:
                self.product_name = raw_prediction["product"]["name"]
            if "version" in raw_prediction["product"]:
                self.product_version = raw_prediction["product"]["version"]

    def __str__(self) -> str:
        rotation_applied_str = "Yes" if self.is_rotation_applied else "No"
        prediction_str = ""
        pages_str = ""
        if self.prediction and len(self.prediction.__str__()) > 0:
            prediction_str = self.prediction.__str__() +"\n"
        if len(self.pages)>0:
            pages_str = "\n".join([page.__str__() for page in self.pages])
        return (
            f"Inference\n"
            f"#########\n"
            f":Product: {self.product_name} v{self.product_version}\n"
            f":Rotation applied: {rotation_applied_str}\n\n"
            f"Prediction\n"
            f"==========\n"
            f"{prediction_str}\n"
            f"Page Predictions\n"
            f"================\n"
            f"{pages_str}"
        )

    @classmethod
    def get_endpoint_info(self) -> Dict[str, str]:
        if self.endpoint_name and self.endpoint_version:
            return {"name": self.endpoint_name, "version": self.endpoint_version}
        raise TypeError("Can't get endpoint information for {self.__name__}")


TypeInference = TypeVar("TypeInference", bound=Inference)
