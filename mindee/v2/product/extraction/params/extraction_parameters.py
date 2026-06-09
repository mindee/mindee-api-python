import json
from dataclasses import dataclass
from typing import ClassVar

from mindee.v2.client_options.base_parameters import BaseParameters
from mindee.v2.product.extraction.params.data_schema import DataSchema


@dataclass
class ExtractionParameters(BaseParameters):
    """Inference parameters to set when sending a file."""

    rag: bool | None = None
    """Enhance extraction accuracy with Retrieval-Augmented Generation."""
    raw_text: bool | None = None
    """Extract the full text content from the document as strings, and fill the ``raw_text`` attribute."""
    polygon: bool | None = None
    """Calculate bounding box polygons for all fields, and fill their ``locations`` attribute."""
    confidence: bool | None = None
    """
    Boost the precision and accuracy of all extractions.
    Calculate confidence scores for all fields, and fill their ``confidence`` attribute.
    """
    text_context: str | None = None
    """
    Additional text context used by the model during inference.
    Not recommended, for specific use only.
    """
    data_schema: DataSchema | str | dict | None = None
    """
    Dynamic changes to the data schema of the model for this inference.
    Not recommended, for specific use only.
    """

    _slug: ClassVar[str] = "inferences"
    """Slug of the endpoint."""

    def __post_init__(self):
        if isinstance(self.data_schema, str):
            self.data_schema = DataSchema(**json.loads(self.data_schema))
        elif isinstance(self.data_schema, dict):
            self.data_schema = DataSchema(**self.data_schema)

    def get_form_data(self) -> dict[str, str | list[str]]:
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
