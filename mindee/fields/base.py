from typing import Optional, Any, List


class Field:
    value: Optional[Any] = None
    confidence: float = 0.0
    bbox: List[List[float]] = []

    def __init__(
        self,
        abstract_prediction,
        value_key="value",
        reconstructed=False,
        extra_fields=None,
        page_n=None,
    ):
        """
        :param abstract_prediction: Prediction object from HTTP response
        :param value_key: Key to use in the abstract_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_n: Page number for multi pages pdf
        :param extra_fields: extra field to get from the abstract_prediction and to set as attribute of the Field
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

        if extra_fields:
            for field_name in extra_fields:
                setattr(self, field_name, abstract_prediction[field_name])

        self.reconstructed = reconstructed

    def __eq__(self, other):
        if self.value is None and other.value is None:
            return True
        if self.value is None or other.value is None:
            return False
        if isinstance(self.value, str):
            return self.value.lower() == other.value.lower()
        return self.value == other.value

    @staticmethod
    def compare_arrays(array1: list, array2: list, attr="value") -> bool:
        """
        :param array1: Array of Fields
        :param array2: Array of Fields
        :param attr: Attribute to compare
        :return: True if all elements in array1 exist in array2, False otherwise
        """
        set1 = set([getattr(f1, attr) for f1 in array1])
        set2 = set([getattr(f2, attr) for f2 in array2])
        return set1 == set2

    @staticmethod
    def array_confidence(array: list) -> float:
        """
        :param array: Array of fields
        :return: Product of all the Fields confidence in the array
        """
        product = 1
        for field in array:
            try:
                product *= field.confidence
            except (AttributeError, TypeError):
                return 0.0
        return float(product)

    @staticmethod
    def array_sum(array: list) -> float:
        """
        :param array: Array of fields
        :return: Sum of all the Fields values in the array
        """
        array_sum = 0
        for field in array:
            try:
                array_sum += field.value
            except (AttributeError, TypeError):
                return 0.0
        return float(array_sum)
