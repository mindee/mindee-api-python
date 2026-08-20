from abc import ABC
from dataclasses import dataclass
from typing import ClassVar

from mindee.client_options.polling_options import PollingOptions


@dataclass
class BaseProductParameters(ABC):
    """Base parameters for sending a file to a Mindee V2 product."""

    model_id: str
    """Model ID to use for the inference. Required."""

    alias: str | None = None
    """
    Optional: a free-form string to tag the request with your own identifier.
    For example, an internal document ID, reference number, or database key.
    If set, it will be included in the job and result responses.
    """

    webhook_ids: list[str] | None = None
    """
    Webhook IDs to call after all processing is finished.
    If empty, no webhooks will be used.
    """

    polling_options: PollingOptions | None = None
    """Options for polling. Set only if having timeout issues."""

    close_file: bool = True
    """Whether to close the file after product."""

    _slug: ClassVar[str]
    """Slug of the product."""

    def get_request_parameters(self) -> dict[str, str | list[str]]:
        """
        Return the parameters as a config dictionary.

        :return: A dict of parameters.
        """
        data: dict[str, str | list[str]] = {
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
