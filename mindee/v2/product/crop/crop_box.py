from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.field.field_location import FieldLocation


class CropBox:
    """Crop inference result."""

    location: FieldLocation
    """Location which includes cropping coordinates for the detected object, within the source document."""
    object_type: str
    """Type or classification of the detected object."""

    def __init__(self, server_response: StringDict):
        self.location = FieldLocation(server_response["location"])
        self.object_type = server_response["object_type"]

    def __str__(self) -> str:
        return f"* :Location: {self.location}\n  :Object Type: {self.object_type}"
