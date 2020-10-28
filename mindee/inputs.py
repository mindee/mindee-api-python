import fitz
import io
import os
from base64 import decodebytes
from mimetypes import guess_type


class Inputs(object):
    def __init__(
            self,
            file,
            input_type="path",
            filename=None,
            cut_pdf=True
    ):
        """
        :param file: Either path or base64 string, or stream
        :param input_type: Specify the type of input fed into the Input
        :param filename: File name of the input
        :param cut_pdf: Automatically reconstruct pdf with more than 4 pages
        """
        self.allowed_extensions = ["image/png", "image/jpg", "image/jpeg", "image/webp", "application/pdf"]
        assert input_type in ["base64", "path", "stream", "dummy"]

        if input_type == "base64":
            # Only for images
            self.file_object = Inputs.b64_to_stream(file)
            self.input_type = input_type
            self.filename = filename
            self.filepath = None
            self.file_extension = 'image/jpg'
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
            self.file_object = ""
            self.input_type = ""
            self.filename = ""
            self.filepath = ""
            self.file_extension = ""
        elif self.file_extension not in self.allowed_extensions:
            raise Exception("File type not allowed, must be in {%s}" % ", ".join(self.allowed_extensions))

        if self.file_extension == "application/pdf" and cut_pdf is True:
            n_pages = self.count_pdf_pages()
            if n_pages > 3:
                self.merge_pdf_pages({0, n_pages - 2, n_pages - 1})

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
    def b64_to_stream(b64_string):
        """
        :param b64_string: image base 64 string
        :return: stream from base64
        """
        bytes_object = decodebytes(b64_string.encode("utf-8"))
        return io.BytesIO(bytes_object)

    def count_pdf_pages(self):
        """
        :return: Number of pages in the Input file for pdfs
        """
        self.file_object.seek(0)
        src = fitz.open(
            stream=self.file_object.read(),
            filetype=self.file_extension,
            filename=self.filename
        )
        return len(src)

    def merge_pdf_pages(self, pages_number):
        """
        :param pages_number: List of pages number to use for merging in the original pdf
        :return: (void) Set the Input.file with the reconstructed pdf stream
        """
        self.file_object.seek(0)
        src = fitz.open(
            stream=self.file_object.read(),
            filetype="pdf"
        )
        doc = fitz.open()
        pdf_pages = [src[n] for n in pages_number]
        for spage in pdf_pages:
            width = spage.MediaBoxSize[0]
            height = spage.MediaBoxSize[1]
            r = fitz.Rect(0, 0, width, height)
            page = doc.newPage(-1, width=width, height=height)
            page.showPDFpage(r, src, spage.number)
        self.file_object.close()
        self.file_object = io.BytesIO(doc.write())

