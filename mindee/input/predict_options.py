from typing import Optional


class PredictOptions:
    """Options to pass to a prediction."""

    def __init__(
        self,
        cropper: bool = False,
        full_text: bool = False,
        include_words: bool = False,
    ):
        self.cropper = cropper
        self.full_text = full_text
        self.include_words = include_words


class AsyncPredictOptions(PredictOptions):
    """Options to pass to an asynchronous prediction."""

    def __init__(
        self,
        cropper: bool = False,
        full_text: bool = False,
        include_words: bool = False,
        workflow_id: Optional[str] = None,
        rag: bool = False,
    ):
        super().__init__(cropper, full_text, include_words)
        self.workflow_id = workflow_id
        self.rag = rag
