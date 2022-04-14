from typing import Any, Dict, List, Optional, TypeVar


class Field:
    value: Optional[Any] = None
    """Raw field value"""
    confidence: float = 0.0
    """Confidence score"""
    bbox: List[List[float]] = []
    """Bounding box coordinates containing the field"""

    def __init__(
        self,
        abstract_prediction: Dict[str, Any],
        value_key: str = "value",
        reconstructed=False,
        page_n: Optional[int] = None,
    ):
        """
        Base field object.

        :param abstract_prediction: Prediction object from HTTP response
        :param value_key: Key to use in the abstract_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_n: Page number for multi-page PDF
        """
        self.page_n = page_n

        if (
            value_key not in abstract_prediction
            or abstract_prediction[value_key] == "N/A"
        ):
            self.value = None
            self.confidence = 0.0
            self.bbox = []
        else:
            self.value = abstract_prediction[value_key]
            try:
                self.confidence = float(abstract_prediction["confidence"])
            except (KeyError, TypeError):
                self.confidence = 0.0
            try:
                self.bbox = abstract_prediction["polygon"]
            except KeyError:
                self.bbox = []

        self.reconstructed = reconstructed

    def __eq__(self, other) -> bool:
        if self.value is None and other.value is None:
            return True
        if self.value is None or other.value is None:
            return False
        if isinstance(self.value, str):
            return self.value.lower() == other.value.lower()
        return self.value == other.value

    def __str__(self) -> str:
        if self.value:
            return f"{self.value}"
        return ""


class TypedField(Field):
    type: str
    """
    The field type as defined by the API.
    This is not a Python base type.
    """

    def __init__(
        self,
        abstract_prediction: Dict[str, Any],
        value_key: str = "value",
        reconstructed=False,
        page_n: Optional[int] = None,
    ):
        super().__init__(abstract_prediction, value_key, reconstructed, page_n)
        self.type = abstract_prediction["type"]

    def __str__(self) -> str:
        if self.value:
            return f"{self.type}: {self.value}"
        return ""


TypeField = TypeVar("TypeField", bound=Field)
TypeFieldList = List[TypeField]


def compare_field_arrays(
    array1: TypeFieldList, array2: TypeFieldList, attr="value"
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
