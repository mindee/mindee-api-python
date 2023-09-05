from typing import Any, Dict, List, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string


class PageGroup:
    """Page Group class for Invoice splitter."""

    page_indexes: List[int] = []
    """Index of each page"""
    confidence: float = 0.0
    """Confidence score"""

    def __init__(self, prediction: Dict[str, Any]):
        self.page_indexes = prediction["page_indexes"]
        try:
            self.confidence = float(prediction["confidence"])
        except (KeyError, TypeError):
            pass

    def __str__(self) -> str:
        return f":Page indexes: {', '.join([str(page_index) for page_index in self.page_indexes])}"


class InvoiceSplitterV1(Document):
    """Invoice Splitter v1 prediction results."""

    invoice_page_groups: List[PageGroup] = []
    """Page groups linked to an invoice."""

    def __init__(
        self,
        api_prediction: TypeApiPrediction,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        super().__init__(
            input_source=input_source,
            document_type="invoice_splitter",
            api_prediction=api_prediction,
            page_n=page_n,
        )
        self._build_from_api_prediction(api_prediction["prediction"])

    def _build_from_api_prediction(
        self, api_prediction: TypeApiPrediction, page_n: Optional[int] = None
    ) -> None:
        """
        Build the object from the prediction API JSON.

        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number
        """
        if (
            "invoice_page_groups" in api_prediction
            and len(api_prediction["invoice_page_groups"]) > 0
        ):
            self.invoice_page_groups = [
                PageGroup(prediction)
                for prediction in api_prediction["invoice_page_groups"]
            ]

    def __str__(self) -> str:
        invoice_page_groups = ""
        if len(self.invoice_page_groups) > 0:
            invoice_page_groups = "\n  "
            invoice_page_groups += f"\n{ ' ' * 2 }".join(
                [str(ivp) for ivp in self.invoice_page_groups]
            )

        return clean_out_string(
            "Invoice Splitter V1 Prediction\n"
            "==============================\n"
            f":Filename: {self.filename or ''}\n"
            f":Invoice Page Groups: {invoice_page_groups}\n"
        )


TypeInvoiceSplitterV1 = TypeVar("TypeInvoiceSplitterV1", bound=InvoiceSplitterV1)
