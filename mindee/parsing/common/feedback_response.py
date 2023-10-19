from mindee.parsing.common.api_response import ApiResponse
from mindee.parsing.common.string_dict import StringDict


class FeedbackResponse(ApiResponse):
    """Wrapper for feedback response."""

    feedback: StringDict

    def __init__(self, server_response: StringDict) -> None:
        """Feedback endpoint."""
        super().__init__(server_response)
        self.feedback = server_response["feedback"]
