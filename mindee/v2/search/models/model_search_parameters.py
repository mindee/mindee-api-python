from dataclasses import dataclass
from typing import ClassVar

from mindee.v2.client_options.base_search_parameters import BaseSearchParameters
from mindee.v2.search.models.model_search_response import ModelSearchResponse


@dataclass(kw_only=True)
class ModelSearchParameters(BaseSearchParameters[ModelSearchResponse]):
    """
    Search for models within the organization linked to the API key.

    All search filters are optional.
    If no search filters are given, all models belonging to the organization are returned.

    Results are paginated.
    """

    name: str | None = None
    """Filter models by partial name match, case-insensitive."""

    model_type: str | None = None
    """Filter by an exact model type."""

    _slug: ClassVar[str] = "models"
    _response_class: type[ModelSearchResponse] = ModelSearchResponse

    def get_request_parameters(self) -> dict[str, str | list[str]]:
        params = super().get_request_parameters()

        if self.name:
            params["name"] = self.name
        if self.model_type:
            params["model_type"] = self.model_type

        return params
