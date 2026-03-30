from pathlib import Path
from typing import List, Union

from mindee.extraction import ExtractedImage


class CropFiles(List[ExtractedImage]):
    """Crop files."""

    def save_all_to_disk(self, path: Union[Path, str]):
        """
        Save all extracted crops to disk.

        :param path: Path to save the extracted splits to
        """
        if isinstance(path, str):
            path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        for idx, split in enumerate(self, start=1):
            split.save_to_file(path / f"crop_{idx:03}.jpg")
