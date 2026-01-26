import json
from dataclasses import dataclass, asdict
from typing import List, Optional, Union

from mindee.input.base_parameters import BaseParameters


@dataclass
class StringDataClass:
    """Base class for dataclasses that can be serialized to JSON."""

    @staticmethod
    def _no_none_values(x) -> dict:
        """Don't include None values in the JSON output."""
        return {k: v for (k, v) in x if v is not None}

    def __str__(self) -> str:
        return json.dumps(
            asdict(self, dict_factory=self._no_none_values), indent=None, sort_keys=True
        )


@dataclass
class DataSchemaField(StringDataClass):
    """A field in the data schema."""

    title: str
    """Display name for the field, also impacts inference results."""
    name: str
    """Name of the field in the data schema."""
    is_array: bool
    """Whether this field can contain multiple values."""
    type: str
    """Data type of the field."""
    classification_values: Optional[List[str]] = None
    """Allowed values when type is `classification`. Leave empty for other types."""
    unique_values: Optional[bool] = None
    """
    Whether to remove duplicate values in the array.
    Only applicable if `is_array` is True.
    """
    description: Optional[str] = None
    """Detailed description of what this field represents."""
    guidelines: Optional[str] = None
    """Optional extraction guidelines."""
    nested_fields: Optional[dict] = None
    """Subfields when type is `nested_object`. Leave empty for other types."""


@dataclass
class DataSchemaReplace(StringDataClass):
    """The structure to completely replace the data schema of the model."""

    fields: List[Union[DataSchemaField, dict]]

    def __post_init__(self) -> None:
        if not self.fields:
            raise ValueError("Data schema replacement fields cannot be empty.")
        if isinstance(self.fields[0], dict):
            self.fields = [
                DataSchemaField(**field)  # type: ignore[arg-type]
                for field in self.fields
            ]


@dataclass
class DataSchema(StringDataClass):
    """Modify the Data Schema."""

    replace: Optional[Union[DataSchemaReplace, dict, str]] = None
    """If set, completely replaces the data schema of the model."""

    def __post_init__(self) -> None:
        if isinstance(self.replace, dict):
            self.replace = DataSchemaReplace(**self.replace)
        elif isinstance(self.replace, str):
            self.replace = DataSchemaReplace(**json.loads(self.replace))


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

    def __post_init__(self):
        if isinstance(self.data_schema, str):
            self.data_schema = DataSchema(**json.loads(self.data_schema))
        elif isinstance(self.data_schema, dict):
            self.data_schema = DataSchema(**self.data_schema)
