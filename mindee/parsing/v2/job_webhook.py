from datetime import datetime
from typing import Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.error_response import ErrorResponse


class JobWebhook:
    """JobWebhook information."""

    id: str
    """JobWebhook ID."""
    created_at: Optional[datetime]
    """Created at date."""
    status: str
    """Status of the webhook."""
    error: Optional[ErrorResponse]
    """Error response, if any."""

    def __init__(self, server_response: StringDict) -> None:
        self.id = server_response["id"]
        self.created_at = self.parse_date(server_response.get("created_at"))
        self.status = server_response["status"]
        self.error = (
            ErrorResponse(server_response["error"])
            if server_response.get("error") is not None
            else None
        )

    @staticmethod
    def parse_date(date_string: Optional[str]) -> Optional[datetime]:
        """Parse the date, if present."""
        if not date_string:
            return None
        date_string = date_string.replace("Z", "+00:00")
        return datetime.fromisoformat(date_string)
