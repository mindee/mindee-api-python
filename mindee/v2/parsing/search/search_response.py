from mindee.v2.search.models.model_search_response import ModelSearchResponse


class SearchResponse(ModelSearchResponse):
    """Models search response."""

    @property
    def pagination_metadata(self):
        """Pagination metadata (Obsolete)."""
        return self.pagination

    @pagination_metadata.setter
    def pagination_metadata(self, value):
        self.pagination = value
