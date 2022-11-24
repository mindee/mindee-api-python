from mindee.endpoints import API_KEY_ENVVAR, BASE_URL_ENVVAR, REQUEST_TIMEOUT_ENVVAR


def clear_envvars(monkeypatch):
    """
    If we have envvars set, the test will pick them up and fail,
    so let's make sure they're empty.
    """
    monkeypatch.setenv(API_KEY_ENVVAR, "")
    monkeypatch.setenv(BASE_URL_ENVVAR, "")
    monkeypatch.setenv(REQUEST_TIMEOUT_ENVVAR, "")


def dummy_envvars(monkeypatch):
    """
    Set all API keys to 'dummy'.
    """
    monkeypatch.setenv(API_KEY_ENVVAR, "dummy")
