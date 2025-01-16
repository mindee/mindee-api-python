import io

from mindee.input.sources.input_type import InputType
from mindee.input.sources.local_input_source import LocalInputSource


class BytesInput(LocalInputSource):
    """Raw bytes input."""

    def __init__(self, raw_bytes: bytes, filename: str) -> None:
        """
        Input document from raw bytes (no buffer).

        :param raw_bytes: Raw data as bytes
        :param filename: File name of the input
        """
        self.file_object = io.BytesIO(raw_bytes)
        self.filename = filename
        self.filepath = None
        super().__init__(input_type=InputType.BYTES)
