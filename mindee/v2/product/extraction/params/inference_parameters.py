import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from mindee.v2.input.base_parameters import BaseParameters
from mindee.v2.product.extraction.params.data_schema import DataSchema


@dataclass
class InferenceParameters(BaseParameters):
    """Inference parameters to set when sending a file."""

    rag: Optional[bool] = None
    """Enhance extraction accuracy with Retrieval-Augmented Generation."""
    raw_text: Optional[bool] = None
    """Extract the full text content from the document as strings, and fill the ``raw_text`` attribute."""
    polygon: Optional[bool] = None
    """Calculate bounding box polygons for all fields, and fill their ``locations`` attribute."""
    confidence: Optional[bool] = None
    """
    Boost the precision and accuracy of all extractions.
    Calculate confidence scores for all fields, and fill their ``confidence`` attribute.
    """
    text_context: Optional[str] = None
    """
    Additional text context used by the model during inference.
    Not recommended, for specific use only.
    """
    data_schema: Optional[Union[DataSchema, str, dict]] = None
    """
    Dynamic changes to the data schema of the model for this inference.
    Not recommended, for specific use only.
    """

    _slug: str = "inferences"
    """Slug of the endpoint."""

    def __post_init__(self):
        if isinstance(self.data_schema, str):
            self.data_schema = DataSchema(**json.loads(self.data_schema))
        elif isinstance(self.data_schema, dict):
            self.data_schema = DataSchema(**self.data_schema)

    def get_form_data(self) -> Dict[str, Union[str, List[str]]]:
        """
        Return the parameters as a config dictionary.

        :return: A dict of parameters.
        """
        data = super().get_form_data()
        if self.data_schema is not None:
            data["data_schema"] = str(self.data_schema)
        if self.rag is not None:
            data["rag"] = data["rag"] = str(self.rag).lower()
        if self.raw_text is not None:
            data["raw_text"] = data["raw_text"] = str(self.raw_text).lower()
        if self.polygon is not None:
            data["polygon"] = data["polygon"] = str(self.polygon).lower()
        if self.confidence is not None:
            data["confidence"] = data["confidence"] = str(self.confidence).lower()
        if self.text_context is not None:
            data["text_context"] = self.text_context
        return data
