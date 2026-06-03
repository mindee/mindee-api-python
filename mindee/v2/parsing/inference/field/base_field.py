from enum import Enum

from mindee.parsing.common import StringDict
from mindee.v2.parsing.inference.field.field_confidence import FieldConfidence
from mindee.v2.parsing.inference.field.field_location import FieldLocation


class FieldType(str, Enum):
    """Field types."""

    OBJECT = "ObjectField"
    LIST = "ListField"
    SIMPLE = "SimpleField"


class BaseField:
    """Field with base information."""

    field_type: FieldType
    _indent_level: int
    locations: list[FieldLocation]
    confidence: FieldConfidence | None

    def __init__(
        self, field_type: FieldType, raw_response: StringDict, indent_level: int = 0
    ) -> None:
        self.field_type = field_type
        self._indent_level = indent_level

        self.confidence = None
        self.locations = []

        if "confidence" in raw_response and raw_response["confidence"] is not None:
            try:
                self.confidence = FieldConfidence(raw_response["confidence"])
            except ValueError:
                self.confidence = None

        if "locations" in raw_response:
            self.locations = []
            for location in raw_response["locations"]:
                self.locations.append(FieldLocation(location))

    def multi_str(self) -> str:
        """String representation of the field in a list."""
        return str(self)
