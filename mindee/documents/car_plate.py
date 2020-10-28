from mindee.documents import Document
from mindee.fields import Field
from mindee.http import request
import os


class CarPlate(Document):
    def __init__(
            self,
            api_prediction=None,
            input_file=None,
            license_plates=None,
            page_n=0
    ):
        """
        :param api_prediction: Raw prediction from HTTP response
        :param input_file: Input object
        :param license_plates: List of license plates values for creating CarPlate object from scratch
        :param page_n: Page number for multi pages pdf input
        """
        self.type = "CarPlate"
        self.license_plates = []

        if api_prediction is not None:
            self.build_from_api_prediction(api_prediction, page_n=page_n)
        else:
            if license_plates is not None:
                self.license_plates = [
                    Field({"value": l}, value_key="value", page_n=page_n) for l in license_plates
                ]

        # Invoke Document constructor
        super(CarPlate, self).__init__(input_file)

        # Run checks
        self._checklist()

        # Reconstruct extra fields
        self._reconstruct()

    def build_from_api_prediction(self, api_prediction, page_n=0):
        """
        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number for multi pages pdf input
        :return: (void) set the object attributes with api prediction values
        """
        self.license_plates = [
            Field(license_plate, page_n=page_n) for license_plate in api_prediction["license_plates"]
        ]

    def __str__(self):
        return "-----Car plate data-----\n" \
               "Filename: %s\n" \
               "Plate: %s\n" \
               "----------------------" % \
               (self.filename, " ".join([l.value for l in self.license_plates]))

    @staticmethod
    def compare(license_plate=None, ground_truth=None):
        """
        :param license_plate: CarPlate object to compare
        :param ground_truth: Ground truth CarPlate object
        :return: Accuracy and precisions metrics
        """
        assert license_plate is not None
        assert ground_truth is not None
        assert isinstance(license_plate, CarPlate)
        assert isinstance(ground_truth, CarPlate)

        metrics = {}

        # Compute Accuracy metrics
        metrics.update(CarPlate.compute_accuracy(license_plate, ground_truth))

        # Compute precision metrics
        metrics.update(CarPlate.compute_precision(license_plate, ground_truth))

        return metrics

    @staticmethod
    def request(input_file, base_url, license_plates_token=None, version="1"):
        """
        Make request to license_plates endpoint
        :param input_file: Input object
        :param base_url: API base URL
        :param license_plates_token: License plate API token
        :param version: API version
        """
        url = os.path.join(base_url, "license_plates", "v" + version, "predict")
        return request(url, input_file, license_plates_token)

    def _checklist(self):
        """
        Call check methods
        """
        pass

    def _reconstruct(self):
        """
        Call fields reconstruction methods
        """
        pass

    @staticmethod
    def compute_accuracy(license_plate, ground_truth):
        """
        :param license_plate: CarPlate object to compare
        :param ground_truth: Ground truth CarPlate object
        :return: Accuracy metrics
        """
        return {
            "__acc__license_plates": Field.compare_arrays(
                license_plate.license_plates, ground_truth.license_plates)
        }

    @staticmethod
    def compute_precision(license_plate, ground_truth):
        """
        :param license_plate: CarPlate object to compare
        :param ground_truth: Ground truth CarPlate object
        :return: Precisions metrics
        """
        precisions = {}

        if len(license_plate.license_plates) == 0:
            precisions["__pre__license_plates"] = None
        else:
            precisions["__pre__license_plates"] = Field.compare_arrays(
                license_plate.license_plates, ground_truth.license_plates)

        return precisions
