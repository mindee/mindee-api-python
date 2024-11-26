from difflib import SequenceMatcher
from pathlib import Path

from mindee.mindee_http.base_settings import (
    API_KEY_ENV_NAME,
    BASE_URL_ENV_NAME,
    REQUEST_TIMEOUT_ENV_NAME,
)


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


EXTRAS_DIR = Path("./tests/data/extras/")


def levenshtein_ratio(ref_str: str, target_str: str) -> float:
    """
    Calculates the Levenshtein ratio between two strings.
    :param ref_str: Reference string.
    :param target_str: Target String.
    :return: Ratio between the two strings
    """
    return SequenceMatcher(None, ref_str, target_str).ratio()
