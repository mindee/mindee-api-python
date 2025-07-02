from datetime import datetime

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.error_response import ErrorResponse


class Webhook:
    """Webhook information for a V2 polling attempt."""

    id: str
    """ID of the webhook."""
    error: ErrorResponse
    """Error response if any."""
    created_at: datetime
    """Date and time the webhook was sent at."""
    status: str
    """Status of the webhook."""

    def __init__(self, raw_response: StringDict) -> None:
        self.id = raw_response["id"]
        self.error = ErrorResponse(raw_response["error"])
        self.created_at = self.parse_date(raw_response["created_at"])
        self.status = raw_response["status"]

    @staticmethod
    def parse_date(date_string: str) -> datetime:
        """Shorthand to parse the date."""
        date_string = date_string.replace("Z", "+00:00")
        return datetime.fromisoformat(date_string)
