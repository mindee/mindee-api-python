from dataclasses import dataclass
from typing import List, Optional

from mindee.input.polling_options import PollingOptions


@dataclass
class InferenceParameters:
    """Inference parameters to set when sending a file."""

    model_id: str
    """ID of the model, required."""
    rag: bool = False
    """If set to `True`, will enable Retrieval-Augmented Generation."""
    alias: Optional[str] = None
    """Use an alias to link the file to your own DB. If empty, no alias will be used."""
    webhook_ids: Optional[List[str]] = None
    """IDs of webhooks to propagate the API response to."""
    polling_options: Optional[PollingOptions] = None
    """Options for polling. Set only if having timeout issues."""
    close_file: bool = True
    """Whether to close the file after parsing."""
