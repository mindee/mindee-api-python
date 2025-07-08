from dataclasses import dataclass
from typing import List, Optional

from mindee.input.page_options import PageOptions
from mindee.input.polling_options import PollingOptions


@dataclass
class InferencePredictOptions:
    """Inference prediction options."""

    model_id: str
    """ID of the model."""
    full_text: bool = False
    """
    Whether to include the full text data for async APIs.
    This performs a full OCR operation on the server and will increase response time and payload size.
    """
    rag: bool = False
    """If set, will enable Retrieval-Augmented Generation."""
    alias: Optional[str] = None
    """Optional alias for the file."""
    webhook_ids: Optional[List[str]] = None
    """IDs of webhooks to propagate the API response to."""
    page_options: Optional[PageOptions] = None
    """Options for page-level inference."""
    polling_options: Optional[PollingOptions] = None
    """Options for polling."""
    close_file: bool = True
    """Whether to close the file after parsing."""
