from dataclasses import dataclass
from typing import List, Optional

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
