from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.error_response import ErrorResponse


class Job:
    """Job information for a V2 polling attempt."""

    id: str
    """Job ID."""
    error: ErrorResponse
    """Error response if any."""
    model_id: str
    """ID of the model."""
    filename: str
    """Name for the file."""
    alias: str
    """Optional alias for the file."""
    status: str
    """Status of the job."""

    def __init__(self, raw_response: StringDict) -> None:
        self.id = raw_response["id"]
        self.status = raw_response["status"]
        self.error = ErrorResponse(raw_response["error"])
        self.model_id = raw_response["model_id"]
        self.filename = raw_response["filename"]
        self.alias = raw_response["alias"]
