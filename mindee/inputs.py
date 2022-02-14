import io
import os
import base64
from typing import Optional, BinaryIO
from mimetypes import guess_type

import pikepdf


ALLOWED_EXTENSIONS = [
    "image/png",
    "image/jpg",
    "image/jpeg",
    "image/webp",
    "application/pdf",
]


class InputDocument:
    file_object: BinaryIO
    filename: str
    input_type: str
    filepath: Optional[str] = None
    cut_pdf: bool
    n_pdf_pages: int

    def __init__(
        self,
        input_type: str,
        cut_pdf=True,
        n_pdf_pages=3,
    ):
        assert 0 < n_pdf_pages <= 3
        self.input_type = input_type
        self.file_extension = guess_type(self.filename)[0]

        if self.file_extension not in ALLOWED_EXTENSIONS and self.input_type != "dummy":
            raise AssertionError(
                "File type not allowed, must be in {%s}" % ", ".join(ALLOWED_EXTENSIONS)
            )

        if self.file_extension == "application/pdf":
            self.check_pdf_open()
            count_pages = self.count_pdf_pages()
            if cut_pdf is True:
                if count_pages > 3:
                    self.merge_pdf_pages(
                        [0, count_pages - 2, count_pages - 1][:n_pdf_pages]
                    )
            if self.is_pdf_empty():
                raise AssertionError(f"PDF pages are empty in: {self.filename}")

    def count_pdf_pages(self):
        """
        :return: Number of pages in the Input file for pdfs
        """
        self.file_object.seek(0)
        with pikepdf.open(self.file_object) as pdf:
            return len(pdf.pages)

    def merge_pdf_pages(self, pages_number):
        """
        :param pages_number: List of pages number to use for merging in the original pdf
        :return: (void) Set the Input.file with the reconstructed pdf stream
        """
        self.file_object.seek(0)
        new_pdf = pikepdf.Pdf.new()
        with pikepdf.open(self.file_object) as pdf:
            for page_n in pages_number:
                new_pdf.pages.append(pdf.pages[page_n])
        self.file_object.close()
        self.file_object = io.BytesIO()
        new_pdf.save(self.file_object)

    def is_pdf_empty(self) -> bool:
        """
        :return: (void) Check if the document contain only empty pages
        """
        self.file_object.seek(0)
        with pikepdf.open(self.file_object) as pdf:
            for page in pdf.pages:

                # mypy incorrectly identifies the "/Length" key's value as
                # an object rather than an int.
                try:
                    total_size = page["/Contents"]["/Length"]
                except ValueError:
                    total_size = 0  # type: ignore
                    for content in page["/Contents"]:  # type: ignore
                        total_size += content["/Length"]
                has_data = total_size > 1000  # type: ignore

                has_font = "/Font" in page["/Resources"].keys()
                has_xobj = "/XObject" in page["/Resources"].keys()

                if has_font or has_xobj or has_data:
                    return False
            return True

    def check_pdf_open(self):
        """
        :return: (void) Check if the document can be opened using pikepdf
        """
        self.file_object.seek(0)
        try:
            pikepdf.open(self.file_object)
        except Exception as err:
            raise RuntimeError("Couldn't open PDF file") from err


class FileDocument(InputDocument):
    def __init__(
        self,
        file: BinaryIO,
        cut_pdf=True,
        n_pdf_pages=3,
    ):
        """
        :param file: FileIO object
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        """
        assert file.name, "File name must be set"

        self.file_object = file
        self.filename = os.path.basename(file.name)
        self.filepath = self.filename

        super().__init__(
            input_type="file",
            cut_pdf=cut_pdf,
            n_pdf_pages=n_pdf_pages,
        )


class PathDocument(InputDocument):
    def __init__(
        self,
        filepath: str,
        cut_pdf=True,
        n_pdf_pages=3,
    ):
        """
        :param filepath: Path to open
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        """
        self.file_object = open(filepath, "rb")  # pylint: disable=consider-using-with
        self.filename = os.path.basename(filepath)
        self.filepath = filepath

        super().__init__(
            input_type="path",
            cut_pdf=cut_pdf,
            n_pdf_pages=n_pdf_pages,
        )


class BytesDocument(InputDocument):
    def __init__(
        self,
        raw_bytes: bytes,
        filename: str,
        cut_pdf=True,
        n_pdf_pages=3,
    ):
        """
        :param raw_bytes: Raw data as bytes
        :param filename: File name of the input
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        """
        self.file_object = io.BytesIO(raw_bytes)

        self.filename = filename
        self.filepath = None

        super().__init__(
            input_type="bytes",
            cut_pdf=cut_pdf,
            n_pdf_pages=n_pdf_pages,
        )


class Base64Document(InputDocument):
    def __init__(
        self,
        base64_string: str,
        filename: str,
        cut_pdf=True,
        n_pdf_pages=3,
    ):
        """
        :param base64_string: Raw data as a base64 encoded string
        :param filename: File name of the input
        :param cut_pdf: Automatically reconstruct pdf with more than N pages
        """
        self.file_object = io.BytesIO(base64.standard_b64decode(base64_string))
        self.filename = filename
        self.filepath = None

        super().__init__(
            input_type="base64",
            cut_pdf=cut_pdf,
            n_pdf_pages=n_pdf_pages,
        )
