from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.search.base_search_response import BaseSearchResponse
from mindee.v2.parsing.search.search_models import SearchModels


class ModelSearchResponse(BaseSearchResponse):
    """Models search response."""

    models: SearchModels
    """Paginated list of matching models."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.models = SearchModels(raw_response["models"])

    def body_lines(self) -> list[str]:
        """Lines composing the response-specific body (header + items)."""
        return ["Models", "######", str(self.models)]
