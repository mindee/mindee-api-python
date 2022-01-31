from typing import Optional, List
from mindee.inputs import Inputs

CUSTOM_DOCUMENT = "custom_document"
OFF_THE_SHELF = "off_the_shelf"


class Endpoint:
    owner: str
    url_name: str
    version: str
    key_name: str
    api_key: str = ""

    def __init__(
        self, owner: str, url_name: str, version: str, key_name: Optional[str] = None
    ):
        """
        :param owner: owner of the product
        :param url_name: name of the product as it appears in the URL
        :param version: interface version
        :param key_name: where to find the key in envvars
        """
        self.owner = owner
        self.url_name = url_name
        self.version = version
        if key_name:
            self.key_name = key_name
        else:
            self.key_name = url_name


class Document:
    type: str

    def __init__(self, input_file: Inputs = None):
        self.filepath = None
        self.filename = None
        self.file_extension = None

        if input_file is not None:
            self.filepath = input_file.filepath
            self.filename = input_file.filename
            self.file_extension = input_file.file_extension
        self.checklist: dict = {}

    @staticmethod
    def request(endpoints: List[Endpoint], input_file):
        """Make request to the product endpoint"""
        raise NotImplementedError()

    def _checklist(self, *args):
        raise NotImplementedError()

    def _reconstruct(self, *args):
        pass

    def all_checks(self):
        """Return all checks"""
        return all(self.checklist)
