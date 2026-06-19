from mindee.parsing.common.common_response import CommonResponse
from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.search.pagination_metadata import PaginationMetadata
from mindee.v2.parsing.search.search_models import SearchModels


class SearchResponse(CommonResponse):
    """Models search response."""

    models: SearchModels
    """Parsed search payload."""
    pagination: PaginationMetadata
    """Pagination metadata for the search results."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.models = SearchModels(raw_response["models"])
        self.pagination = PaginationMetadata(raw_response["pagination"])

    def __str__(self) -> str:
        """
        String representation.
        """
        return "\n".join(
            [
                "Models",
                "######",
                str(self.models),
                "Pagination Metadata",
                "###################",
                str(self.pagination),
                "",
            ]
        )
