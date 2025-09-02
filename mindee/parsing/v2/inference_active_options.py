from mindee.parsing.common.string_dict import StringDict


class InferenceActiveOptions:
    """Active options for the inference."""

    raw_text: bool
    polygon: bool
    confidence: bool
    rag: bool

    def __init__(self, raw_response: StringDict):
        self.raw_text = raw_response["raw_text"]
        self.polygon = raw_response["polygon"]
        self.confidence = raw_response["confidence"]
        self.rag = raw_response["rag"]

    def __str__(self) -> str:
        return (
            f"Active Options\n=============="
            f"\n:Raw Text: {self.raw_text}"
            f"\n:Polygon: {self.polygon}"
            f"\n:Confidence: {self.confidence}"
            f"\n:RAG: {self.rag}"
        )
