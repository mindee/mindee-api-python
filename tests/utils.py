from mindee.endpoints import MINDEE_API_KEY_NAME


def clear_envvars(monkeypatch):
    """
    If we have envvars set, the test will pick them up and fail,
    so let's make sure they're empty.
    """
    monkeypatch.setenv(MINDEE_API_KEY_NAME, "")


def dummy_envvars(monkeypatch):
    """
    Set all API keys to 'dummy'.
    """
    monkeypatch.setenv(MINDEE_API_KEY_NAME, "dummy")
