import os
from difflib import SequenceMatcher
from pathlib import Path

from mindee.v1.mindee_http.base_settings import (
    API_KEY_ENV_NAME,
    BASE_URL_ENV_NAME,
    REQUEST_TIMEOUT_ENV_NAME,
)

RESOURCE_PATH = Path(__file__).parent / "data"
FILE_TYPES_PATH = RESOURCE_PATH / "file_types"
OUTPUT_PATH = RESOURCE_PATH / "output"

V1_RESOURCE_PATH = RESOURCE_PATH / "v1"
V1_ERROR_PATH = V1_RESOURCE_PATH / "errors"
V1_PRODUCT_PATH = V1_RESOURCE_PATH / "products"
V1_EXTRAS_PATH = V1_RESOURCE_PATH / "extras"

V2_RESOURCE_PATH = RESOURCE_PATH / "v2"
V2_PRODUCT_PATH = V2_RESOURCE_PATH / "products"


def clear_envvars(monkeypatch) -> None:
    """
    If we have envvars set, the test will pick them up and fail,
    so let's make sure they're empty.
    """
    monkeypatch.setenv(API_KEY_ENV_NAME, "")
    monkeypatch.setenv(BASE_URL_ENV_NAME, "")
    monkeypatch.setenv(REQUEST_TIMEOUT_ENV_NAME, "")


def dummy_envvars(monkeypatch) -> None:
    """
    Set all API keys to 'dummy'.
    """
    monkeypatch.setenv(API_KEY_ENV_NAME, "dummy")


def levenshtein_ratio(ref_str: str, target_str: str) -> float:
    """
    Calculates the Levenshtein ratio between two strings.
    :param ref_str: Reference string.
    :param target_str: Target String.
    :return: Ratio between the two strings
    """
    return SequenceMatcher(None, ref_str, target_str).ratio()


def cleanup_output_files(created_files):
    for file_path in created_files:
        full_path = OUTPUT_PATH / file_path
        if full_path.exists():
            os.remove(full_path)
