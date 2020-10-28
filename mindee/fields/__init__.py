class Field(object):
    def __init__(
            self,
            abstract_prediction,
            value_key="value",
            reconstructed=False,
            extra_fields=None,
            page_n=None
    ):
        """
        :param abstract_prediction: Prediction object from HTTP response
        :param value_key: Key to use in the abstract_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_n: Page number for multi pages pdf
        :param extra_fields: extra field to get from the abstract_prediction and to set as attribute of the Field
        """
        self.page_n = page_n
        if value_key not in abstract_prediction or abstract_prediction[value_key] == "N/A":
            self.value = None
            self.probability = 0.
            self.bbox = []
        else:
            self.value = abstract_prediction[value_key]

            if "probability" in abstract_prediction:
                self.probability = abstract_prediction["probability"]
            else:
                self.probability = 0.

            if "segmentation" in abstract_prediction:
                self.bbox = abstract_prediction["segmentation"]["bounding_box"]
            else:
                self.bbox = []

        if extra_fields:
            for field_name in extra_fields:
                setattr(self, field_name, abstract_prediction[field_name])

        self.reconstructed = reconstructed

    def __eq__(self, other):
        if self.value is None and other.value is None:
            return True
        elif self.value is None or other.value is None:
            return False
        else:
            if type(self.value) == str:
                return self.value.lower() == other.value.lower()
            else:
                return self.value == other.value

    @staticmethod
    def compare_arrays(array1, array2, attr="value"):
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
    def array_probability(array):
        """
        :param array: Array of fields
        :return: Product of all the Fields probability in the array
        """
        product = 1
        for field in array:
            try:
                product *= field.probability
            except:
                return 0.
        return product

    @staticmethod
    def array_sum(array):
        """
        :param array: Array of fields
        :return: Sum of all the Fields values in the array
        """
        array_sum = 0
        for field in array:
            try:
                array_sum += field.value
            except:
                return 0.
        return array_sum

