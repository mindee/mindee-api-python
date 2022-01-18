import io
import os
import base64
from mimetypes import guess_type
import pikepdf

ALLOWED_EXTENSIONS = [
    "image/png",
    "image/jpg",
    "image/jpeg",
    "image/webp",
    "application/pdf",
]


class Inputs:
    def __init__(
        self, file, input_type="path", filename=None, cut_pdf=True, n_pdf_pages=3
    ):
        """
        :param file: Either path or base64 string, or stream
        :param input_type: Specify the type of input fed into the Input
        :param filename: File name of the input
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        """
        assert input_type in ["base64", "path", "stream", "dummy"]
        assert 0 < n_pdf_pages <= 3

        if input_type == "base64":
            assert filename, "filename must be set"
            # Only for images
            self.file_object = Inputs.b64_to_stream(file)
            self.input_type = input_type
            self.filename = filename
            self.filepath = None
            self.file_extension = "image/jpg"
        elif input_type == "stream":
            # Case input is a file object
            self.file_object = file
            self.input_type = input_type
            self.filename = os.path.basename(file.name)
            self.filepath = file.name
            self.file_extension = guess_type(file.name)[0]
        elif input_type == "path":
            # Case input is a path
            self.file_object = open(file, "rb")
            self.input_type = input_type
            self.filename = os.path.basename(file)
            self.filepath = file
            self.file_extension = guess_type(file)[0]

        if input_type == "dummy":
            self.file_object = None
            self.input_type = ""
            self.filename = ""
            self.filepath = ""
            self.file_extension = ""
        elif self.file_extension not in ALLOWED_EXTENSIONS:
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

            self.check_if_document_is_empty()

    @staticmethod
    def load(input_type, filename, filepath, file_extension):
        """
        :param input_type: Specify the type of input fed into the Input
        :param filename: File name of the input
        :param filepath: Original file path of the Input file
        :param file_extension: Extension of the file
        :return: Dummy Input object to use when restoring Response from json file
        """
        file_input = Inputs(filename, input_type="dummy")
        file_input.input_type = input_type
        file_input.filepath = filepath
        file_input.file_extension = file_extension
        return file_input

    @staticmethod
    def b64_to_stream(b64_string: str):
        """
        :param b64_string: image base 64 string
        :return: stream from base64
        """
        bytes_object = base64.standard_b64decode(b64_string)
        return io.BytesIO(bytes_object)

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

    def check_if_document_is_empty(self):
        """
        :return: (void) Check if the document contain only empty pages
        """
        self.file_object.seek(0)
        with pikepdf.open(self.file_object) as pdf:
            for _, page in enumerate(pdf.pages):
                if (
                    "/Font" in page["/Resources"].keys()
                    or "/XObject" in page["/Resources"].keys()
                    or page["/Contents"]["/Length"] > 1000
                ):
                    return
            raise Exception("PDF pages are empty")

    def check_pdf_open(self):
        """
        :return: (void) Check if the document can be opened using pikepdf
        """
        self.file_object.seek(0)
        try:
            pikepdf.open(self.file_object)
        except Exception as err:
            raise Exception("Couldn't open PDF file. %s" % err)
