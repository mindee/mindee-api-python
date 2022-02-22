from typing import Dict, List

from mindee.http import Endpoint
from mindee.documents.base import TypeDocument


class DocumentConfig:
    document_type: str
    endpoints: List[Endpoint]
    singular_name: str
    plural_name: str
    constructor: TypeDocument

    def __init__(
        self,
        document_type: str,
        singular_name: str,
        plural_name: str,
        constructor: TypeDocument,
        endpoints: List[Endpoint],
    ):
        self.document_type = document_type
        self.singular_name = singular_name
        self.plural_name = plural_name
        self.constructor = constructor
        self.endpoints = endpoints


DocumentConfigDict = Dict[tuple, DocumentConfig]
