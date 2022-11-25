from typing import Any, Dict, List, Optional, TypeVar

from mindee.geometry import Point, Polygon, Quadrilateral, get_bounding_box

TypePrediction = Dict[str, Any]


class FieldPositionMixin:
    bounding_box: Optional[Quadrilateral]
    """A right rectangle containing the word in the document."""
    polygon: Polygon
    """A polygon containing the word in the document."""

    def _set_position(self, prediction: TypePrediction):
        self.bounding_box = None
        self.polygon = Polygon()
        try:
            self.polygon = Polygon(
                Point(point[0], point[1]) for point in prediction["polygon"]
            )
        except KeyError:
            pass
        if self.polygon:
            self.bounding_box = get_bounding_box(self.polygon)


class BaseField:
    value: Optional[Any] = None
    """Raw field value"""
    confidence: float = 0.0
    """Confidence score"""
    reconstructed: bool
    """Whether the field was reconstructed from other fields."""
    page_n: Optional[int] = None
    """The document page on which the information was found."""

    def __init__(
        self,
        prediction: TypePrediction,
        value_key: str = "value",
        reconstructed: bool = False,
        page_n: Optional[int] = None,
    ):
        """
        Base field object.

        :param prediction: Prediction object from HTTP response
        :param value_key: Key to use in the abstract_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_n: Page number for multi-page PDF
        """
        if page_n is None:
            try:
                self.page_n = prediction["page_id"]
            except KeyError:
                pass
        else:
            self.page_n = page_n

        self.reconstructed = reconstructed

        if value_key not in prediction or prediction[value_key] == "N/A":
            return

        self.value = prediction[value_key]
        try:
            self.confidence = float(prediction["confidence"])
        except (KeyError, TypeError):
            pass

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


TypeBaseField = TypeVar("TypeBaseField", bound=BaseField)
TypeFieldList = List[TypeBaseField]


def compare_field_arrays(
    array1: TypeFieldList, array2: TypeFieldList, attr: str = "value"
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


def field_array_confidence(array: TypeFieldList) -> float:
    """
    Multiply all Field's confidence in the array.

    :param array: Array of fields
    :return: Product as float
    """
    product = 1
    for field in array:
        try:
            product *= field.confidence
        except (AttributeError, TypeError):
            return 0.0
    return float(product)


def field_array_sum(array: TypeFieldList) -> float:
    """
    Add all the Field values in the array.

    :param array: Array of fields
    :return: Sum as `float`.
    """
    arr_sum = 0
    for field in array:
        try:
            arr_sum += field.value
        except (AttributeError, TypeError):
            return 0.0
    return float(arr_sum)
