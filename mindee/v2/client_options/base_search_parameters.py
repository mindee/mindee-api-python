from abc import ABC
from dataclasses import dataclass
from typing import ClassVar, Generic, TypeVar

from mindee.v2.parsing.search.base_search_response import BaseSearchResponse

TypeSearchResponse = TypeVar("TypeSearchResponse", bound=BaseSearchResponse)


@dataclass(kw_only=True)
class BaseSearchParameters(ABC, Generic[TypeSearchResponse]):
    """Base parameters for searches."""

    page: int | None = None
    """1-based page index."""

    per_page: int | None = None
    """Number of items per page."""

    _slug: ClassVar[str]
    """Slug of the searchable resource."""

    _response_class: type[TypeSearchResponse]
    """Response class for the search."""

    def get_request_parameters(self) -> dict[str, str | list[str]]:
        """
        Gets the request parameters for the search request.

        :return: A dict of parameters.
        """
        data: dict[str, str | list[str]] = {}

        if self.page is not None:
            data["page"] = str(self.page)
        if self.per_page is not None:
            data["per_page"] = str(self.per_page)

        return data

    def get_slug(self) -> str:
        """Gets the slug of the resource."""
        return self._slug

    def get_response_class(self) -> type[TypeSearchResponse]:
        """Gets the response class for the search."""
        return self._response_class
