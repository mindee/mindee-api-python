class CancellationToken:
    """Custom cancellation token that can be used to cancel a polling request."""

    is_canceled: bool
    """A cancellation token that can be used to cancel a request."""

    def __init__(
        self,
        is_canceled: bool = False,
    ):
        self.is_canceled = is_canceled

    def cancel(self):
        """Cancel the request."""
        self.is_canceled = True
