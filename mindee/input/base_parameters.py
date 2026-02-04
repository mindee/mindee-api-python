from abc import ABC
from dataclasses import dataclass, field
from typing import Dict, Optional, List, Union

from mindee.input.polling_options import PollingOptions


@dataclass
class BaseParameters(ABC):
    """Base class for parameters accepted by all V2 endpoints."""

    _slug: str = field(init=False)
    """Slug of the endpoint."""

    model_id: str
    """ID of the model, required."""
    alias: Optional[str] = None
    """Use an alias to link the file to your own DB. If empty, no alias will be used."""
    webhook_ids: Optional[List[str]] = None
    """IDs of webhooks to propagate the API response to."""
    polling_options: Optional[PollingOptions] = None
    """Options for polling. Set only if having timeout issues."""
    close_file: bool = True
    """Whether to close the file after product."""

    def get_form_data(self) -> Dict[str, Union[str, List[str]]]:
        """
        Return the parameters as a config dictionary.

        :return: A dict of parameters.
        """
        data: Dict[str, Union[str, List[str]]] = {
            "model_id": self.model_id,
        }
        if self.alias is not None:
            data["alias"] = self.alias
        if self.webhook_ids and len(self.webhook_ids) > 0:
            data["webhook_ids"] = self.webhook_ids
        return data

    @classmethod
    def get_enqueue_slug(cls) -> str:
        """Getter for the enqueue slug."""
        return cls._slug
