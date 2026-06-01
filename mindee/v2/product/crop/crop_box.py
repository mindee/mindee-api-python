from mindee.extraction import ExtractedImage, extract_multiple_images_from_source
from mindee.input import LocalInputSource
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.field import FieldLocation
from mindee.parsing.v2.inference_response import InferenceResponse


class CropBox:
    """Deprecated class. Use CropItem instead."""

    location: FieldLocation
    """Location which includes cropping coordinates for the detected object, within the source document."""

    object_type: str
    """Type or classification of the detected object."""

    extraction_response: InferenceResponse | None = None
    """The extraction response associated with the crop."""

    def __init__(self, server_response: StringDict):
        self.location = FieldLocation(server_response["location"])
        self.object_type = server_response["object_type"]
        if server_response.get("extraction_response") is not None:
            self.extraction_response = InferenceResponse(
                server_response["extraction_response"]
            )

    def __str__(self) -> str:
        return f"* :Location: {self.location}\n  :Object Type: {self.object_type}"

    def extract_from_file(self, input_source: LocalInputSource) -> ExtractedImage:
        """
        Apply the split range inference to a file and return a single extracted PDF.

        :param input_source: Local file to apply the inference to
        :return: Extracted PDF
        """
        return extract_multiple_images_from_source(
            input_source, self.location.page, [self.location.polygon]
        )[0]
