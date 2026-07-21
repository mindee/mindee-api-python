from datetime import datetime

from mindee.parsing.common.common_response import CommonResponse
from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.error.error_response import ErrorResponse


class FailedInferenceResponse(CommonResponse):
    """Webhook payload returned when an inference fails before producing a result."""

    inference_id: str
    """UUID of the failed inference."""
    model_id: str
    """UUID of the model used."""
    file_name: str
    """Name of the input file."""
    file_alias: str
    """Alias sent for the file, if any."""
    error: ErrorResponse
    """Problem details for the failure, if available."""
    created_at: datetime
    """Date and time when the inference was started."""

    def __init__(self, raw_prediction: StringDict) -> None:
        super().__init__(raw_prediction)
        self.inference_id = raw_prediction["inference_id"]
        self.model_id = raw_prediction["model_id"]
        self.file_name = raw_prediction["file_name"]
        self.file_alias = raw_prediction["file_alias"]
        self.error = ErrorResponse(raw_prediction["error"])
        self.created_at = datetime.fromisoformat(
            raw_prediction["created_at"].replace("Z", "+00:00")
        )
