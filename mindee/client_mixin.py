from mindee.error import MindeeClientError


class ClientMixin:
    """Mixin for clients V1 & V2 common static methods."""

    @staticmethod
    def _validate_async_params(
        initial_delay_sec: float, delay_sec: float, max_retries: int
    ) -> None:
        min_delay = 1
        min_initial_delay = 1
        min_retries = 1
        if delay_sec < min_delay:
            raise MindeeClientError(
                f"Cannot set auto-parsing delay to less than {min_delay} second(s)."
            )
        if initial_delay_sec < min_initial_delay:
            raise MindeeClientError(
                f"Cannot set initial parsing delay to less than {min_initial_delay} second(s)."
            )
        if max_retries < min_retries:
            raise MindeeClientError(f"Cannot set retries to less than {min_retries}.")
