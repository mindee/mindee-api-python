from dataclasses import dataclass

from mindee.v2.client_options.base_product_parameters import BaseProductParameters


@dataclass
class BaseClassificationProductParameters(BaseProductParameters):
    """Base parameters for classification-based products."""

    extraction_text_context: str | None = None
    """Pass additional context to the extraction model chained to this utility inference."""

    def get_request_parameters(self) -> dict[str, str | list[str]]:
        data = super().get_request_parameters()
        if self.extraction_text_context is not None:
            data["extraction_text_context"] = self.extraction_text_context
        return data
