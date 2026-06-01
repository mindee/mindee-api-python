from mindee.parsing.common import ExecutionPriority


class WorkflowOptions:
    """Options to pass to a workflow execution."""

    alias: str | None
    """Alias for the document."""
    priority: ExecutionPriority | None
    """Priority of the document."""
    full_text: bool
    """Whether to include the full OCR text response in compatible APIs."""
    public_url: str | None
    """A unique, encrypted URL for accessing the document validation interface without requiring authentication."""
    rag: bool
    """Whether to enable Retrieval-Augmented Generation."""

    def __init__(
        self,
        alias: str | None = None,
        priority: ExecutionPriority | None = None,
        full_text: bool | None = False,
        public_url: str | None = None,
        rag: bool | None = False,
    ):
        self.alias = alias
        self.priority = priority
        self.full_text = full_text if full_text else False
        self.public_url = public_url
        self.rag = rag if rag else False
