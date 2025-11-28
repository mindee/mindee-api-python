from mindee.parsing.common.string_dict import StringDict


class InferenceActiveOptions:
    """Active options for the inference."""

    raw_text: bool
    """
    Whether the Raw Text feature was activated.
    When this feature is activated, the raw text extracted from the document is returned in the result.
    """
    polygon: bool
    """
    Whether the polygon feature was activated.
    When this feature is activated, the bounding-box polygon(s) for each field is returned in the result.
    """
    confidence: bool
    """
    Whether the confidence feature was activated.
    When this feature is activated, a confidence score for each field is returned in the result.
    """
    rag: bool
    """
    Whether the Retrieval-Augmented Generation feature was activated.
    When this feature is activated, the RAG pipeline is used to increase result accuracy.
    """
    text_context: bool
    """
    Whether the text context feature was activated.
    When this feature is activated, the provided context is used to improve the accuracy of the inference.
    """

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
