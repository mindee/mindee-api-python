from mindee.parsing.common import CommonResponse
from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.error.error_item import ErrorItem


class ErrorResponse(CommonResponse):
    """Error response detailing a problem. The format adheres to RFC 9457."""

    status: int
    """The HTTP status code returned by the server."""
    detail: str
    """A human-readable explanation specific to the occurrence of the problem."""
    title: str
    """A short, human-readable summary of the problem."""
    code: str
    """A machine-readable code specific to the occurrence of the problem."""
    errors: list[ErrorItem]
    """A list of explicit error details."""

    def __init__(self, raw_response: StringDict):
        super().__init__(raw_response)
        self.status = raw_response["status"]
        self.detail = raw_response["detail"]
        self.title = raw_response["title"]
        self.code = raw_response["code"]
        try:
            self.errors = [ErrorItem(error) for error in raw_response["errors"]]
        except KeyError:
            self.errors = []

    def __str__(self) -> str:
        """To make the error prettier to display."""

        result = [
            "Error Details",
            "=============",
            f":HTTP Status: {self.status}",
            f":Title: {self.title}",
            f":Code: {self.code}",
            f":Detail: {self.detail}",
        ]

        if self.errors:
            result.append("")
            result.append("Error Items")
            result.append("-----------")

            for i, error in enumerate(self.errors):
                result.append(f"**Error {i + 1}:**")
                result.append(f"  :Pointer: {getattr(error, 'pointer', '')}")
                result.append(f"  :Detail: {getattr(error, 'detail', '')}")

                if i < len(self.errors) - 1:
                    result.append("")

        return "\n".join(result) + "\n"
