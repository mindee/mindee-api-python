from mindee.parsing.common.string_dict import StringDict


class DataSchemaActiveOptions:
    """Data schema options activated during the inference."""

    replace: bool

    def __init__(self, raw_response: StringDict):
        self.replace = raw_response["replace"]

    def __str__(self) -> str:
        return f"Data Schema\n-----------\n:Replace: {self.replace}"


class InferenceActiveOptions:
    """Active options for the inference."""

    raw_text: bool
    """Extract the full text content from the document as strings, and fill the ``raw_text`` attribute."""
    polygon: bool
    """Calculate bounding box polygons for all fields, and fill their ``locations`` attribute."""
    confidence: bool
    """
    Boost the precision and accuracy of all extractions.
    Calculate confidence scores for all fields, and fill their ``confidence`` attribute.
    """
    rag: bool
    """Enhance extraction accuracy with Retrieval-Augmented Generation."""
    text_context: bool
    """
    Whether the text context feature was activated.
    When this feature is activated, the provided context is used to improve the accuracy of the inference.
    """
    data_schema: DataSchemaActiveOptions
    """Data schema options provided for the inference."""

    def __init__(self, raw_response: StringDict):
        self.raw_text = raw_response["raw_text"]
        self.polygon = raw_response["polygon"]
        self.confidence = raw_response["confidence"]
        self.rag = raw_response["rag"]
        self.text_context = raw_response["text_context"]
        self.data_schema = DataSchemaActiveOptions(raw_response["data_schema"])

    def __str__(self) -> str:
        return (
            f"Active Options\n=============="
            f"\n:Raw Text: {self.raw_text}"
            f"\n:Polygon: {self.polygon}"
            f"\n:Confidence: {self.confidence}"
            f"\n:RAG: {self.rag}"
            f"\n:Text Context: {self.text_context}"
            f"\n\n{self.data_schema}"
        )
