from abc import ABC, abstractmethod

from mindee.parsing.common import StringDict
from mindee.parsing.common.common_response import CommonResponse
from mindee.v2.parsing.search.pagination_metadata import PaginationMetadata


class BaseSearchResponse(CommonResponse, ABC):
    """Base class for search responses."""

    pagination: PaginationMetadata
    """Pagination metadata for the search results."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.pagination = PaginationMetadata(raw_response["pagination"])

    @abstractmethod
    def body_lines(self) -> list[str]:
        """List of strings representing the search response."""

    def __str__(self) -> str:
        """
        String representation.
        """
        lines: list[str] = self.body_lines()
        lines += ["Pagination Metadata", "###################", str(self.pagination)]
        return "\n".join(lines)
