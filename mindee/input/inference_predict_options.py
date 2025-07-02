from dataclasses import dataclass
from typing import List, Optional


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
