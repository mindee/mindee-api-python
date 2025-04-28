from typing import Dict, Generic, List, Optional, Type, TypeVar

from mindee.error.mindee_error import MindeeError
from mindee.parsing.common.extras import Extras
from mindee.parsing.common.page import TypePage
from mindee.parsing.common.prediction import TypePrediction
from mindee.parsing.common.product import Product
from mindee.parsing.common.string_dict import StringDict


class Inference(Generic[TypePrediction, TypePage]):
    """Base Inference class for all predictions."""

    product: Product
    """Name and version of a given product, as sent back by the API."""
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
    page_id: Optional[int]
    """Optional page id for page-level predictions."""
    extras: Optional[Extras] = None
    """Potential Extras fields sent back along with the prediction."""

    def __init__(self, raw_prediction: StringDict, page_id: Optional[int] = None):
        self.is_rotation_applied = None
        if "is_rotation_applied" in raw_prediction:
            self.is_rotation_applied = raw_prediction["is_rotation_applied"]
        self.product = Product(raw_prediction["product"])
        if page_id:
            self.page_id = page_id

        if "extras" in raw_prediction and raw_prediction["extras"]:
            self.extras = Extras(raw_prediction["extras"])

    def __str__(self) -> str:
        rotation_applied_str = "Yes" if self.is_rotation_applied else "No"
        prediction_str = ""
        pages_str = ""
        if self.prediction and len(str(self.prediction)) > 0:
            prediction_str = f"{str(self.prediction)}\n"
        if len(self.pages) > 0:
            pages_str = "\nPage Predictions\n================\n\n" + "\n".join(
                [str(page) for page in self.pages]
            )
        return (
            f"Inference\n"
            f"#########\n"
            f":Product: {self.product}\n"
            f":Rotation applied: {rotation_applied_str}\n\n"
            f"Prediction\n"
            f"==========\n"
            f"{prediction_str}"
            f"{pages_str}"
        )

    @staticmethod
    def get_endpoint_info(klass: Type["Inference"]) -> Dict[str, str]:
        """
        Retrieves the endpoint information for an Inference.

        Should never retrieve info for CustomV1, as a custom endpoint should be created to use CustomV1.

        :param klass: product subclass to access endpoint information.
        """
        if klass.endpoint_name and klass.endpoint_version:
            return {"name": klass.endpoint_name, "version": klass.endpoint_version}
        raise MindeeError("Can't get endpoint information for {klass.__name__}")


TypeInference = TypeVar("TypeInference", bound=Inference)
