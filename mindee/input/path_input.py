import os
from pathlib import Path

from mindee.input.local_input_source import LocalInputSource


class PathInput(LocalInputSource):
    """A local path input."""

    def __init__(self, filepath: Path | str) -> None:
        """
        Input document from a path.

        :param filepath: Path to open
        """
        self.file_object = open(filepath, "rb")  # noqa: SIM115 # pylint: disable=consider-using-with
        self.filename = os.path.basename(Path(filepath))
        self.filepath = str(filepath)
        super().__init__()
