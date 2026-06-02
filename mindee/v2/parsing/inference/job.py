from datetime import datetime

from mindee.parsing.common import StringDict
from mindee.v2.parsing.inference.error_response import ErrorResponse
from mindee.v2.parsing.inference.job_webhook import JobWebhook


class Job:
    """Job information for a V2 polling attempt."""

    id: str
    """Job ID."""
    error: ErrorResponse | None
    """Error response if any."""
    created_at: datetime
    """Date and time of the Job creation."""
    completed_at: datetime | None = None
    """Date and time of the Job completion. Filled once processing is finished."""
    model_id: str
    """ID of the model."""
    filename: str
    """Name for the file."""
    alias: str
    """Optional alias for the file."""
    status: str
    """Status of the job."""
    polling_url: str
    """URL to poll for the job status."""
    result_url: str | None
    """URL to poll for the job result, redirects to the result if available."""
    webhooks: list[JobWebhook]
    """ID of webhooks associated with the job."""

    def __init__(self, raw_response: StringDict) -> None:
        self.id = raw_response["id"]
        self.status = raw_response["status"]
        self.error = (
            ErrorResponse(raw_response["error"]) if raw_response["error"] else None
        )
        self.created_at = datetime.fromisoformat(
            raw_response["created_at"].replace("Z", "+00:00")
        )
        completed_at = raw_response.get("completed_at")
        if completed_at:
            self.completed_at = datetime.fromisoformat(
                completed_at.replace("Z", "+00:00")
            )
        self.model_id = raw_response["model_id"]
        self.polling_url = raw_response["polling_url"]
        self.filename = raw_response["filename"]
        self.result_url = raw_response["result_url"]
        self.alias = raw_response["alias"]
        self.webhooks = [
            JobWebhook(webhook) for webhook in raw_response.get("webhooks", [])
        ]
