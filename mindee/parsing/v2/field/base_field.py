from typing import List, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.field.dynamic_field import DynamicField, FieldType
from mindee.parsing.v2.field.field_confidence import FieldConfidence
from mindee.parsing.v2.field.field_location import FieldLocation


class BaseField(DynamicField):
    """Field with base information."""

    locations: List[FieldLocation]
    confidence: Optional[FieldConfidence]

    def __init__(
        self, field_type: FieldType, raw_response: StringDict, indent_level: int = 0
    ) -> None:
        super().__init__(field_type, indent_level)
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
