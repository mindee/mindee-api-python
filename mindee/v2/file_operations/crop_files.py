from pathlib import Path
from typing import List, Union

from mindee.image.extracted_image import ExtractedImage


class CropFiles(List[ExtractedImage]):
    """Crop files."""

    def save_all_to_disk(self, path: Union[Path, str], prefix: str = "crop"):
        """
        Save all extracted crops to disk.

        :params path: Path to save the extracted splits to.
        :params prefix: Prefix to add to the filename, defaults to 'crop'.
        """
        if isinstance(path, str):
            path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        for idx, split in enumerate(self, start=1):
            split.save_to_file(path / f"{prefix}_{idx:03}.jpg")
