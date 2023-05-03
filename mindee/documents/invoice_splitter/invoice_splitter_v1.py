from typing import Any, Dict, List, Optional, TypeVar, Union

from mindee.documents.base import Document, TypeApiPrediction
from mindee.input.sources import LocalInputSource, UrlInputSource


class PageGroup:
    page_indexes: List[int] = []
    confidence: int

    def __init__(self, prediction: Dict[str, Any]):
        self.page_indexes = prediction["page_indexes"]
        self.confidence = prediction["confidence"]

    def __str__(self) -> str:
        return f"page indexes: {', '.join([str(page_index) for page_index in self.page_indexes])}"


class InvoiceSplitterV1(Document):
    invoice_page_groups: List[PageGroup] = []

    def __init__(
        self,
        api_prediction: Dict[str, Any],
        input_source: Union[LocalInputSource, UrlInputSource],
        page_n: int,
    ):
        super().__init__(
            input_source=input_source,
            document_type="shipping_container",
            api_prediction=api_prediction,
            page_n=page_n,
        )
        self._build_from_api_prediction(api_prediction["prediction"], page_n=page_n)

    def _build_from_api_prediction(
        self, api_prediction: TypeApiPrediction, page_n: Optional[int] = None
    ) -> None:
        """
        Build the object from the prediction API JSON.

        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number
        """
        if (
            api_prediction["invoice_page_groups"]
            and len(api_prediction["invoice_page_groups"]) > 0
        ):
            self.invoice_page_groups = [
                PageGroup(prediction)
                for prediction in api_prediction["invoice_page_groups"]
            ]

    def __str__(self) -> str:
        invoice_page_groups = "\n"
        if len(self.invoice_page_groups) > 0:
            invoice_page_groups += "\n ".join(
                [str(ivp) for ivp in self.invoice_page_groups]
            )

        out_str = (
            f"----- Invoice Splitter V1 -----"
            f"Filename: {self.filename}"
            f"Invoice Page Groups: {invoice_page_groups}"
            f"----------------------"
        )
        return out_str


TypeInvoiceSplitterV1 = TypeVar("TypeInvoiceSplitterV1", bound=InvoiceSplitterV1)
