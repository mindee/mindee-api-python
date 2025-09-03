from dataclasses import dataclass
from typing import List, Optional

from mindee.input.polling_options import PollingOptions


@dataclass
class InferenceParameters:
    """Inference parameters to set when sending a file."""

    model_id: str
    """ID of the model, required."""
    rag: Optional[bool] = None
    """Enhance extraction accuracy with Retrieval-Augmented Generation."""
    raw_text: Optional[bool] = None
    """Extract the full text content from the document as strings, and fill the ``raw_text`` attribute."""
    polygon: Optional[bool] = None
    """Calculate bounding box polygons for all fields, and fill their ``locations`` attribute."""
    confidence: Optional[bool] = None
    """
    Boost the precision and accuracy of all extractions.
    Calculate confidence scores for all fields, and fill their ``confidence`` attribute.
    """
    alias: Optional[str] = None
    """Use an alias to link the file to your own DB. If empty, no alias will be used."""
    webhook_ids: Optional[List[str]] = None
    """IDs of webhooks to propagate the API response to."""
    polling_options: Optional[PollingOptions] = None
    """Options for polling. Set only if having timeout issues."""
    close_file: bool = True
    """Whether to close the file after parsing."""
