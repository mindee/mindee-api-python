from dataclasses import dataclass
from typing import List, Optional

from mindee.input.polling_options import PollingOptions


@dataclass
class InferenceParameters:
    """Inference parameters to set when sending a file."""

    model_id: str
    """ID of the model, required."""
    rag: bool = False
    """Use Retrieval-Augmented Generation during inference."""
    raw_text: bool = False
    """Extract the entire text from the document as strings, and fill the ``raw_text`` attribute."""
    polygon: bool = False
    """Calculate bounding box polygons for values, and fill the ``locations`` attribute of fields"""
    confidence: bool = False
    """
    Calculate confidence scores for values, and fill the ``confidence`` attribute of fields.
    Useful for automation.
    """
    alias: Optional[str] = None
    """Use an alias to link the file to your own DB. If empty, no alias will be used."""
    webhook_ids: Optional[List[str]] = None
    """IDs of webhooks to propagate the API response to."""
    polling_options: Optional[PollingOptions] = None
    """Options for polling. Set only if having timeout issues."""
    close_file: bool = True
    """Whether to close the file after parsing."""
