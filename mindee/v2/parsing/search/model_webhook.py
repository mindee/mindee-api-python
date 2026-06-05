class ModelWebhook:
    """Model webhook information."""

    id: str
    """ID of the webhook."""
    name: str
    """Name of the webhook."""
    url: str
    """URL of the webhook."""

    def __init__(self, server_response: dict) -> None:
        self.id = server_response["id"]
        self.name = server_response["name"]
        self.url = server_response["url"]

    def __str__(self) -> str:
        return f":Name: {self.name}\n:ID: {self.id}\n:URL: {self.url}"
