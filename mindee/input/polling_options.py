class PollingOptions:
    """Options for asynchronous polling."""

    initial_delay_sec: float
    """Initial delay before the first polling attempt."""
    delay_sec: float
    """Delay between each polling attempts."""
    max_retries: int
    """Total amount of polling attempts."""

    def __init__(
        self,
        initial_delay_sec: float = 2,
        delay_sec: float = 1.5,
        max_retries: int = 80,
    ):
        self.initial_delay_sec = initial_delay_sec
        self.delay_sec = delay_sec
        self.max_retries = max_retries
