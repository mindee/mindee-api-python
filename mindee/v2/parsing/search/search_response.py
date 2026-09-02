import warnings

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.search.pagination_metadata import PaginationMetadata
from mindee.v2.search.models.model_search_response import ModelSearchResponse


class SearchResponse(ModelSearchResponse):
    """Deprecated: use `ModelSearchResponse` instead."""

    def __init__(self, raw_response: StringDict) -> None:
        warnings.warn(
            "SearchResponse is deprecated, use ModelSearchResponse instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(raw_response)

    @property
    def pagination_metadata(self) -> PaginationMetadata:
        """Pagination metadata (Obsolete)."""
        warnings.warn(
            "pagination_metadata is deprecated, use pagination instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.pagination

    @pagination_metadata.setter
    def pagination_metadata(self, value: PaginationMetadata) -> None:
        warnings.warn(
            "pagination_metadata is deprecated, use pagination instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.pagination = value
