from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.search.paginationmetadata import PaginationMetadata
from mindee.v2.parsing.search.search_models import SearchModels


class SearchResponse:
    """Models search response."""

    models: SearchModels
    """Parsed search payload."""
    pagination: PaginationMetadata
    """Pagination metadata for the search results."""

    def __init__(self, raw_response: StringDict) -> None:
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
