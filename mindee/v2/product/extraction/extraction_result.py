from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference.field import InferenceFields
from mindee.v2.parsing.inference.field.factory import parse_field
from mindee.v2.parsing.inference.rag_metadata import RAGMetadata
from mindee.v2.parsing.inference.raw_text import RawText


class ExtractionResult:
    """Inference result info."""

    fields: InferenceFields
    """Fields contained in the inference."""
    raw_text: RawText | None = None
    """Potential options retrieved alongside the inference."""
    rag: RAGMetadata | None = None
    """RAG metadata."""

    def __init__(self, raw_response: StringDict) -> None:
        self.fields = InferenceFields(raw_response["fields"], parse_field)
        if raw_response.get("raw_text"):
            self.raw_text = RawText(raw_response["raw_text"])
        if raw_response.get("rag"):
            self.rag = RAGMetadata(raw_response["rag"])

    def __str__(self) -> str:
        out_str = f"Fields\n======{self.fields}"
        return out_str
