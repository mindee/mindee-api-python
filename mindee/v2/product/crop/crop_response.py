from mindee.input.sources.local_input_source import LocalInputSource
from mindee.parsing.common.string_dict import StringDict
from mindee.v2.file_operations.crop_files import CropFiles
from mindee.v2.parsing.inference import BaseResponse
from mindee.v2.product.crop.crop_inference import CropInference


class CropResponse(BaseResponse):
    """Represent a crop inference response from Mindee V2 API."""

    inference: CropInference
    """Inference object for crop inference."""

    _slug: str = "products/crop/results"
    """Slug of the inference."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.inference = CropInference(raw_response["inference"])

    def extract_from_file(self, input_source: LocalInputSource) -> CropFiles:
        """
        Apply the crop inference to a file and return a list of extracted images.

        :param input_source: Local file to apply the inference to
        :return: List of extracted PDFs
        """
        return CropFiles(
            [
                crop.extract_from_file(input_source)
                for crop in self.inference.result.crops
            ]
        )
