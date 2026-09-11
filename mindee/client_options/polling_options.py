from mindee.error import MindeeClientError


class PollingOptions:
    """Options for asynchronous polling."""

    initial_delay_sec: float
    """Initial delay before the first polling attempt."""
    delay_sec: float
    """Delay between each polling attempt."""
    max_retries: int
    """Total number of polling attempts."""

    def __init__(
        self,
        initial_delay_sec: float = 2,
        delay_sec: float = 1.5,
        max_retries: int = 80,
    ):
        self.initial_delay_sec = initial_delay_sec
        self.delay_sec = delay_sec
        self.max_retries = max_retries

    def validate_settings(self) -> None:
        """Validates polling options against minimum accepted values."""

        min_delay = 1
        min_initial_delay = 1
        min_retries = 1
        if self.delay_sec < min_delay:
            raise MindeeClientError(
                f"Cannot set auto-parsing delay to less than {min_delay} second(s)."
            )
        if self.initial_delay_sec < min_initial_delay:
            raise MindeeClientError(
                f"Cannot set initial parsing delay to less than {min_initial_delay} second(s)."
            )
        if self.max_retries < min_retries:
            raise MindeeClientError(f"Cannot set retries to less than {min_retries}.")
