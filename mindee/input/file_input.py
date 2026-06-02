import io
import os
from typing import BinaryIO, IO, Union, cast

from mindee.input.local_input_source import LocalInputSource


class FileInput(LocalInputSource):
    """A binary file input."""

    def __init__(self, file: Union[BinaryIO, IO[bytes]]) -> None:
        """
        Input document from a Python binary file object.

        Note: the calling function is responsible for closing the file.

        :params file: FileIO object
        """
        assert file.name, "File name must be set"

        if hasattr(file, "seek") and callable(file.seek):
            try:
                file.seek(0)
            except (io.UnsupportedOperation, OSError):
                pass
        self.file_object = cast(BinaryIO, file)
        self.filename = os.path.basename(file.name)
        self.filepath = file.name
        super().__init__()
