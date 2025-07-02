class ErrorResponse(RuntimeError):
    """Error response info."""

    detail: str
    """Detail relevant to the error."""

    status: int
    """Http error code."""

    def __str__(self):
        return f"HTTP Status: {self.status} - {self.detail}"
