import json
from dataclasses import dataclass, asdict

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
    classification_values: list[str] | None = None
    """Allowed values when type is `classification`. Leave empty for other types."""
    unique_values: bool | None = None
    """
    Whether to remove duplicate values in the array.
    Only applicable if `is_array` is True.
    """
    description: str | None = None
    """Detailed description of what this field represents."""
    guidelines: str | None = None
    """Optional extraction guidelines."""
    nested_fields: dict | None = None
    """Subfields when type is `nested_object`. Leave empty for other types."""


@dataclass
class DataSchemaReplace(StringDataClass):
    """The structure to completely replace the data schema of the model."""

    fields: list[DataSchemaField | dict]

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

    replace: DataSchemaReplace | dict | str | None = None
    """If set, completely replaces the data schema of the model."""

    def __post_init__(self) -> None:
        if isinstance(self.replace, dict):
            self.replace = DataSchemaReplace(**self.replace)
        elif isinstance(self.replace, str):
            self.replace = DataSchemaReplace(**json.loads(self.replace))


@dataclass
class InferenceParameters(BaseParameters):
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

    _slug: str = "inferences"
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
