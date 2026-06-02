from pathlib import Path

from mindee.pdf.extracted_pdf import ExtractedPDF


class SplitFiles(list[ExtractedPDF]):
    """Split files."""

    def save_all_to_disk(self, path: str | Path, prefix: str = "split"):
        """
        Save all extracted splits to disk.

        :param path: Path to save the extracted splits to.
        :param prefix: Prefix to add to the filename, defaults to 'split'.
        """
        if isinstance(path, str):
            path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        for idx, split in enumerate(self, start=1):
            split.save_to_file(path / f"{prefix}_{idx:03}.pdf")
