import json
from datetime import datetime
from typing import Optional

from mindee.parsing.common.string_dict import StringDict


class Job:
    """
    Job class for asynchronous requests.

    Will hold information on the queue a document has been submitted to.
    """

    id: str
    """ID of the job sent by the API in response to an enqueue request."""
    error: Optional[StringDict] = None
    """Information about an error that occurred during the job processing."""
    issued_at: datetime
    """Timestamp of the request reception by the API."""
    available_at: Optional[datetime] = None
    """Timestamp of the request after it has been completed."""
    status: str
    """Status of the request, as seen by the API."""
    millisecs_taken: int
    """Time (ms) taken for the request to be processed by the API."""

    def __init__(self, json_response: dict) -> None:
        """
        Wrapper for the HTTP response sent from the API when a document is enqueued.

        :param json_response: JSON response sent by the server
        """
        self.issued_at = datetime.fromisoformat(json_response["issued_at"])
        if json_response.get("available_at"):
            self.available_at = datetime.fromisoformat(json_response["available_at"])
        else:
            self.available_at = None
        self.id = json_response["id"]
        if json_response.get("status_code"):
            self.status_code = json_response["status_code"]
        if json_response.get("error"):
            self.error = json_response.get("error")
        self.status = json_response["status"]
        if self.available_at:
            self.millisecs_taken = int(
                (self.available_at - self.issued_at).total_seconds() * 1000
            )

    def __str__(self) -> str:
        return json.dumps(self.__dict__, indent=4, sort_keys=True, default=str)
