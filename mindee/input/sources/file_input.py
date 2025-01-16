import os
from typing import BinaryIO

from mindee.input.sources.input_type import InputType
from mindee.input.sources.local_input_source import LocalInputSource


class FileInput(LocalInputSource):
    """A binary file input."""

    def __init__(self, file: BinaryIO) -> None:
        """
        Input document from a Python binary file object.

        Note: the calling function is responsible for closing the file.

        :param file: FileIO object
        """
        assert file.name, "File name must be set"

        self.file_object = file
        self.filename = os.path.basename(file.name)
        self.filepath = file.name
        super().__init__(input_type=InputType.FILE)
