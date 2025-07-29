from mindee.parsing.common.string_dict import StringDict


class InferenceModel:
    """Inference model info."""

    id: str
    """ID of the model."""

    def __init__(self, raw_response: StringDict) -> None:
        self.id = raw_response["id"]

    def __str__(self) -> str:
        return f"Model\n=====" f"\n:ID: {self.id}"
