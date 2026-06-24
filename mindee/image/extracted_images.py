from pathlib import Path

from mindee.image.extracted_image import ExtractedImage


class ExtractedImages(list[ExtractedImage]):
    """List of extracted images."""

    def save_all_to_disk(self, output_path: Path | str) -> None:
        """Save all extracted images to disk."""
        for image in self:
            image.save_to_file(output_path)
