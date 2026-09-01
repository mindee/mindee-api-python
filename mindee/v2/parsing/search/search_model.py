from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.search.model_webhook import ModelWebhook


class SearchModel:
    """Individual model information."""

    id: str
    """ID of the model."""
    name: str
    """Name of the model."""
    model_type: str
    """Type of the model."""
    webhooks: list[ModelWebhook]
    """List of webhooks associated with the model."""

    def __init__(self, server_response: StringDict) -> None:
        self.id = server_response["id"]
        self.name = server_response["name"]
        self.model_type = server_response["model_type"]
        self.webhooks = (
            [ModelWebhook(webhook) for webhook in server_response["webhooks"]]
            if "webhooks" in server_response
            else []
        )

    def __str__(self) -> str:
        """String representation of the model."""
        return f":Name: {self.name}\n:ID: {self.id}\n:Model Type: {self.model_type}"

    def to_list_string(self) -> list[str]:
        """Return a list of display lines for multi-line rendering."""
        return [
            f":Name: {self.name}",
            f":ID: {self.id}",
            f":Model Type: {self.model_type}",
        ]
