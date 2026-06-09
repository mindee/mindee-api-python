from mindee.parsing.common.string_dict import StringDict
from mindee.v2.product.classification.classification_classifier import (
    ClassificationClassifier,
)


class ClassificationResult:
    """Classification result info."""

    classification: ClassificationClassifier

    def __init__(self, raw_response: StringDict) -> None:
        self.classification = ClassificationClassifier(raw_response["classification"])

    def __str__(self) -> str:
        return f"Classification\n======{self.classification}"
