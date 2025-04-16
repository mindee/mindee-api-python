from typing import Optional

from mindee.parsing.common import ExecutionPriority


class WorkflowOptions:
    """Options to pass to a workflow execution."""

    alias: Optional[str]
    """Alias for the document."""
    priority: Optional[ExecutionPriority]
    """Priority of the document."""
    full_text: bool
    """Whether to include the full OCR text response in compatible APIs."""
    public_url: Optional[str]
    """A unique, encrypted URL for accessing the document validation interface without requiring authentication."""
    rag: bool
    """Whether to enable Retrieval-Augmented Generation."""

    def __init__(
        self,
        alias: Optional[str] = None,
        priority: Optional[ExecutionPriority] = None,
        full_text: Optional[bool] = False,
        public_url: Optional[str] = None,
        rag: Optional[bool] = False,
    ):
        self.alias = alias
        self.priority = priority
        self.full_text = full_text if full_text else False
        self.public_url = public_url
        self.rag = rag if rag else False
