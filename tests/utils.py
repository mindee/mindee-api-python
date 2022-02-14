def clear_envvars(monkeypatch):
    """
    If we have envvars set, the test will pick them up and fail,
    so let's make sure they're empty.
    """
    monkeypatch.setenv("MINDEE_RECEIPT_API_KEY", "")
    monkeypatch.setenv("MINDEE_INVOICE_API_KEY", "")
    monkeypatch.setenv("MINDEE_PASSPORT_API_KEY", "")
    monkeypatch.setenv("MINDEE_DUMMY_DUMMY_API_KEY", "")


def dummy_envvars(monkeypatch):
    """
    Set all API keys to 'dummy'.
    """
    monkeypatch.setenv("MINDEE_RECEIPT_API_KEY", "dummy")
    monkeypatch.setenv("MINDEE_INVOICE_API_KEY", "dummy")
    monkeypatch.setenv("MINDEE_PASSPORT_API_KEY", "dummy")
    monkeypatch.setenv("MINDEE_DUMMY_DUMMY_API_KEY", "dummy")
