from mindee.parsing.common.string_dict import StringDict


class InferenceActiveOptions:
    """Active options for the inference."""

    raw_text: bool
    """Whether raw text extraction is active or not."""
    polygon: bool
    """Whether polygon extraction is active or not."""
    confidence: bool
    """Whether confidence scores are active or not."""
    rag: bool
    """Whether RAG is active or not."""
    text_context: bool
    """Whether text context is active or not."""

    def __init__(self, raw_response: StringDict):
        self.raw_text = raw_response["raw_text"]
        self.polygon = raw_response["polygon"]
        self.confidence = raw_response["confidence"]
        self.rag = raw_response["rag"]
        self.text_context = raw_response["text_context"]

    def __str__(self) -> str:
        return (
            f"Active Options\n=============="
            f"\n:Raw Text: {self.raw_text}"
            f"\n:Polygon: {self.polygon}"
            f"\n:Confidence: {self.confidence}"
            f"\n:RAG: {self.rag}"
        )
