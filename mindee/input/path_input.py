import os
from pathlib import Path
from typing import Union

from mindee.input.local_input_source import LocalInputSource


class PathInput(LocalInputSource):
    """A local path input."""

    def __init__(self, filepath: Union[Path, str]) -> None:
        """
        Input document from a path.

        :params filepath: Path to open
        """
        self.file_object = open(filepath, "rb")  # pylint: disable=consider-using-with
        self.filename = os.path.basename(filepath)
        self.filepath = str(filepath)
        super().__init__()
