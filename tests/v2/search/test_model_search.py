import pytest

from mindee.input import LocalResponse
from mindee.v2.search.models.model_search_response import ModelSearchResponse
from tests.utils import V2_DATA_DIR


@pytest.mark.v2
def test_should_load_search_models_locally():
    file_path = V2_DATA_DIR / "search" / "models.json"
    local_response = LocalResponse(file_path)
    response = local_response.deserialize_response(ModelSearchResponse)

    assert isinstance(response, ModelSearchResponse)

    assert len(response.models) == 5
    assert response.pagination.total_items == 5
    assert response.pagination.page == 1
    assert response.pagination.per_page == 50
    assert response.pagination.total_pages == 1

    first_item = response.models[0]
    assert first_item.name == "Extraction With Webhooks"
    assert first_item.id == "afde5151-aa11-aa11-9289-fa04e50ca3b9"
    assert first_item.model_type == "extraction"

    assert len(first_item.webhooks) == 2
    assert first_item.webhooks[0].id == "a2286ed9-aa11-aa11-bdc5-2f8496c5641a"
    assert first_item.webhooks[0].name == "FAILURE"
    assert first_item.webhooks[0].url == "https://failure.mindee.com"

    last_item = response.models[-1]
    assert last_item.name == "Extraction Without Webhooks Key"
    assert last_item.id == "e14e0923-ee55-ee55-a335-8d2110917d7b"
