from pathlib import Path

from mindee.pdf.extracted_pdf import ExtractedPDF


class ExtractedPDFs(list[ExtractedPDF]):
    """List of extracted PDFs."""

    def save_all_to_disk(self, output_path: Path | str) -> None:
        """Save all extracted images to disk."""

        for image in self:
            image.save_to_file(output_path)
