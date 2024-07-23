from typing import Any, List, Optional, Type

from mindee.geometry.point import Point
from mindee.geometry.polygon import Polygon
from mindee.geometry.quadrilateral import Quadrilateral, get_bounding_box
from mindee.parsing.common.string_dict import StringDict


class FieldPositionMixin:
    """Mixin class to add position information."""

    bounding_box: Optional[Quadrilateral]
    """A right rectangle containing the word in the document."""
    polygon: Polygon
    """A polygon containing the word in the document."""

    def _set_position(self, raw_prediction: StringDict):
        self.bounding_box = None
        self.polygon = Polygon()
        try:
            self.polygon = Polygon(
                Point(point[0], point[1]) for point in raw_prediction["polygon"]
            )
        except (KeyError, TypeError):
            pass
        if self.polygon:
            self.bounding_box = get_bounding_box(self.polygon)
        else:
            self.bounding_box = None


class FieldConfidenceMixin:
    """Mixin class to add a confidence score."""

    confidence: float
    """The confidence score."""

    def _set_confidence(self, raw_prediction: StringDict):
        try:
            self.confidence = float(raw_prediction["confidence"])
        except (KeyError, TypeError):
            self.confidence = 0.0


class BaseField(FieldConfidenceMixin):
    """Base class for most fields."""

    value: Optional[Any]
    """Raw field value"""
    reconstructed: bool
    """Whether the field was reconstructed from other fields."""
    page_id: Optional[int]
    """The document page on which the information was found."""

    def __init__(
        self,
        raw_prediction: StringDict,
        value_key: str = "value",
        reconstructed: bool = False,
        page_id: Optional[int] = None,
    ):
        self.value = None
        self.confidence = 0.0
        """
        Base field object.

        :param raw_prediction: Prediction object from HTTP response
        :param value_key: Key to use in the abstract_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_id: Page number for multi-page PDF
        """
        if page_id is None:
            try:
                self.page_id = raw_prediction["page_id"]
            except (KeyError, TypeError):
                pass
        else:
            self.page_id = page_id

        self.reconstructed = reconstructed

        if value_key not in raw_prediction or raw_prediction[value_key] == "N/A":
            return

        self.value = raw_prediction[value_key]
        self._set_confidence(raw_prediction)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BaseField):
            return NotImplemented
        if self.value is None and other.value is None:
            return True
        if self.value is None or other.value is None:
            return False
        if isinstance(self.value, str):
            return self.value.lower() == other.value.lower()
        return self.value == other.value

    def __str__(self) -> str:
        if self.value is not None:
            return f"{self.value}"
        return ""


def compare_field_arrays(
    array1: List[Type[BaseField]], array2: List[Type[BaseField]], attr: str = "value"
) -> bool:
    """
    Check that all elements are present in both arrays.

    :param array1: Array of Fields
    :param array2: Array of Fields
    :param attr: Attribute to compare
    :return: True if all elements in array1 exist in array2, False otherwise
    """
    set1 = {getattr(f1, attr) for f1 in array1}
    set2 = {getattr(f2, attr) for f2 in array2}
    return set1 == set2


def field_array_confidence(array: List[Type[BaseField]]) -> float:
    """
    Multiply all Field's confidence in the array.

    :param array: Array of fields
    :return: Product as float
    """
    product: float = 1
    for field in array:
        try:
            product *= field.confidence
        except (AttributeError, TypeError):
            return 0.0
    return float(product)


def field_array_sum(array: List[Type[BaseField]]) -> float:
    """
    Add all the Field values in the array.

    :param array: Array of fields
    :return: Sum as `float`.
    """
    arr_sum = 0
    for field in array:
        try:
            if field.value is None:
                raise TypeError
            arr_sum += field.value
        except (AttributeError, TypeError):
            return 0.0
    return arr_sum


def float_to_string(value: Optional[float], min_precision=2) -> str:
    """Print a float with a specified minimum precision, but allowing greater precision."""
    if value is None:
        return ""

    precision = len(str(value).split(".")[1])
    precision = max(precision, min_precision)
    return f"{value:.{precision}f}"


def int_to_string(value: Optional[int]) -> str:
    """Print an integer as a string."""
    if value is None:
        return ""

    return f"{value}"


def bool_to_string(value: Optional[bool]) -> str:
    """Print a boolean as a string."""
    if value is None:
        return ""

    return f"{value}"


def to_opt_float(raw_prediction: StringDict, key: str) -> Optional[float]:
    """Make sure a prediction value is either a ``float`` or ``None``."""
    try:
        return float(raw_prediction[key])
    except TypeError:
        return None


def to_opt_int(raw_prediction: StringDict, key: str) -> Optional[int]:
    """Make sure a prediction value is either an ``int`` or ``None``."""
    try:
        return int(raw_prediction[key])
    except TypeError:
        return None


def to_opt_bool(raw_prediction: StringDict, key: str) -> Optional[bool]:
    """Make sure a prediction value is either a ``bool`` or ``None``."""
    try:
        return bool(raw_prediction[key])
    except TypeError:
        return None
