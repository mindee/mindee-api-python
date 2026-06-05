from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.search.model_webhook import ModelWebhook


class SearchModel:
    """Individual model information."""

    id: str
    """Model ID."""
    name: str
    """Model name."""
    model_type: str
    """Model type."""
    webhooks: list[ModelWebhook]
    """Webhooks associated with the model."""

    def __init__(self, server_response: StringDict) -> None:
        self.id = server_response["id"]
        self.name = server_response["name"]
        self.model_type = server_response["model_type"]
        self.webhooks = (
            [ModelWebhook(webhook) for webhook in server_response["webhooks"]]
            if "webhooks" in server_response
            else []
        )
