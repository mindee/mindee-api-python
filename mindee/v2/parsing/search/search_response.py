from mindee.v2.parsing.search.pagination_metadata import PaginationMetadata
from mindee.v2.search.models.model_search_response import ModelSearchResponse


class SearchResponse(ModelSearchResponse):
    """Models search response."""

    @property
    def pagination_metadata(self) -> PaginationMetadata:
        """Pagination metadata (Obsolete)."""
        return self.pagination

    @pagination_metadata.setter
    def pagination_metadata(self, value: PaginationMetadata) -> None:
        self.pagination = value
