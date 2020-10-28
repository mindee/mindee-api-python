import copy


class Document(object):
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
        raise NotImplementedError()

    def _checklist(self, *args):
        raise NotImplementedError()

    def _reconstruct(self, *args):
        pass

    def all_checks(self):
        return all(self.checklist)

    @staticmethod
    def merge_pages(page_documents):
        """
        :param page_documents: Document object list
        :return: A single Document where each field is set with the maximum probability field
        """
        document = copy.deepcopy(page_documents[0])
        attributes = [a for a in dir(document)]
        for doc in page_documents:
            for attribute in attributes:
                if not hasattr(getattr(doc, attribute), "probability"):
                    continue

                if getattr(doc, attribute).probability > getattr(document, attribute).probability:
                    setattr(document, attribute, getattr(doc, attribute))

        return document
