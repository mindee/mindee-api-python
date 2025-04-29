from typing import Optional

from mindee.parsing.common.string_dict import StringDict


class RagExtra:
    """Contains information on the Retrieval-Augmented-Generation of a prediction."""

    matching_document_id: Optional[str] = None

    def __init__(self, raw_prediction: StringDict) -> None:
        if raw_prediction and "matching_document_id" in raw_prediction:
            self.matching_document_id = raw_prediction["matching_document_id"]
