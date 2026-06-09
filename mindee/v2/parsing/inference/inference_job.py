from mindee.parsing.common.string_dict import StringDict


class InferenceJob:
    """Inference Job info."""

    id: str
    """UUID of the Job."""

    def __init__(self, raw_response: StringDict) -> None:
        self.id = raw_response["id"]

    def __str__(self) -> str:
        return f"Job\n===\n:ID: {self.id}"
