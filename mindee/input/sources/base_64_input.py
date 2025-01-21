import base64
import io

from mindee.input.sources.input_type import InputType
from mindee.input.sources.local_input_source import LocalInputSource


class Base64Input(LocalInputSource):
    """Base64-encoded text input."""

    def __init__(self, base64_string: str, filename: str) -> None:
        """
        Input document from a base64 encoded string.

        :param base64_string: Raw data as a base64 encoded string
        :param filename: File name of the input
        """
        self.file_object = io.BytesIO(base64.standard_b64decode(base64_string))
        self.filename = filename
        self.filepath = None
        super().__init__(input_type=InputType.BASE64)
