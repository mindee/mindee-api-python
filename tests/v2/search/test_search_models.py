import json

import pytest

from mindee.v2.parsing.search.search_response import SearchResponse
from tests.utils import V2_DATA_DIR


@pytest.mark.v2
def test_search_models():
    data_file = V2_DATA_DIR / "search" / "models.json"
    json_file = data_file.read_text()
    models_json = json.loads(json_file)
    models_response = SearchResponse(models_json)

    assert len(models_response.models) == models_response.pagination.total_items == 5
    assert models_response.pagination.page == 1
    assert models_response.pagination.per_page == 50
    assert models_response.pagination.total_pages == 1
    assert models_response.pagination.total_items_unfiltered is None

    assert models_response.models[0].name == "Extraction With Webhooks"
    assert models_response.models[0].id == "afde5151-aa11-aa11-9289-fa04e50ca3b9"
    assert models_response.models[0].model_type == "extraction"
    assert len(models_response.models[0].webhooks) == 2
    assert (
        models_response.models[0].webhooks[0].id
        == "a2286ed9-aa11-aa11-bdc5-2f8496c5641a"
    )
    assert models_response.models[0].webhooks[0].name == "FAILURE"
    assert models_response.models[0].webhooks[0].url == "https://failure.mindee.com"
    assert models_response.models[-1].name == "Extraction Without Webhooks Key"
    assert models_response.models[-1].id == "e14e0923-ee55-ee55-a335-8d2110917d7b"
