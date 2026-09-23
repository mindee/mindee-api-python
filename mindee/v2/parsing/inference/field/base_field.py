from enum import Enum
from typing import TYPE_CHECKING, ClassVar, TypeAlias, Union

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference.field.field_confidence import FieldConfidence
from mindee.v2.parsing.inference.field.field_location import FieldLocation


class FieldType(str, Enum):
    """Field types."""

    OBJECT = "ObjectField"
    LIST = "ListField"
    SIMPLE = "SimpleField"


if TYPE_CHECKING:
    from mindee.v2.parsing.inference.field.list_field import ListField
    from mindee.v2.parsing.inference.field.object_field import ObjectField
    from mindee.v2.parsing.inference.field.simple_field import SimpleField


ResultFieldsType: TypeAlias = Union["SimpleField", "ObjectField", "ListField"]


class BaseField:
    """Base class for V2 fields."""

    field_type: FieldType
    """The type of field."""
    locations: list[FieldLocation]
    """List of the location candidates for the value."""
    confidence: FieldConfidence | None
    """Confidence associated with the field."""
    _indent_level: int
    """For pretty printing."""

    _registry: ClassVar[dict[str, type[ResultFieldsType]]] = {}

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

    @classmethod
    def register(cls, discriminator_key: str):
        """Class decorator: subclasses declare which JSON key identifies them."""

        def decorator(subclass):
            cls._registry[discriminator_key] = subclass
            return subclass

        return decorator

    @classmethod
    def build(cls, raw_response: dict, indent_level: int) -> ResultFieldsType:
        """Build an instance of the appropriate subclass."""

        if not isinstance(raw_response, dict):
            raise ValueError("Field must be a dict")
        for key, subclass in cls._registry.items():
            if key in raw_response:
                return subclass(raw_response, indent_level)
        raise ValueError("Invalid structure for field")

    def multi_str(self) -> str:
        """String representation of the field in a list."""
        return str(self)
