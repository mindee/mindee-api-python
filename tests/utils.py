from mindee.mindee_http.mindee_api import (
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
