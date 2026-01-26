from abc import ABC
from dataclasses import dataclass
from typing import Optional, List

from mindee.input.polling_options import PollingOptions


@dataclass
class BaseParameters(ABC):
    """Base class for parameters accepted by all V2 endpoints."""

    model_id: str
    """ID of the model, required."""
    alias: Optional[str] = None
    """Use an alias to link the file to your own DB. If empty, no alias will be used."""
    webhook_ids: Optional[List[str]] = None
    """IDs of webhooks to propagate the API response to."""
    polling_options: Optional[PollingOptions] = None
    """Options for polling. Set only if having timeout issues."""
    close_file: bool = True
    """Whether to close the file after parsing."""
