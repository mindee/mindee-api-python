from typing import List, TypeVar

from mindee.parsing.common import StringDict
from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.product.invoice_splitter.invoice_splitter_v1_document import InvoiceSplitterV1Document

class InvoiceSplitterV1(Inference):
    """Inference prediction for Invoice Splitter, API version 1."""
    
    prediction: InvoiceSplitterV1Document
    pages: List[Page[InvoiceSplitterV1Document]]
    endpoint_name = "invoice_splitter"
    endpoint_version = "1"
    
    def __init__(self,
                 raw_prediction: StringDict):
        super().__init__(raw_prediction)
        self.prediction = InvoiceSplitterV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            self.pages.append(Page(InvoiceSplitterV1Document, page, page["id"], page["orientation"]))
    

TypeInvoiceSplitterV1 = TypeVar("TypeInvoiceSplitterV1", bound=InvoiceSplitterV1)
