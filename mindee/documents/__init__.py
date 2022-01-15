class Document:
    def __init__(self, input_file=None):
        self.filepath = None
        self.filename = None
        self.file_extension = None

        if input_file is not None:
            self.filepath = input_file.filepath
            self.filename = input_file.filename
            self.file_extension = input_file.file_extension
        self.checklist = {}

    def request(self, *args):
        """Make request to the product endpoint"""
        raise NotImplementedError()

    def _checklist(self, *args):
        raise NotImplementedError()

    def _reconstruct(self, *args):
        pass

    def all_checks(self):
        """Return all checks"""
        return all(self.checklist)
