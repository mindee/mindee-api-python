from dataclasses import dataclass

from mindee.v2.product.extraction.params.string_data_class import StringDataClass


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
