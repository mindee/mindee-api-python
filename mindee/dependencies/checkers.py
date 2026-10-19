from mindee.error.mindee_dependency_error import MindeeDependencyError

try:
    import bernard_ledit  # noqa: F401 #pylint: disable=unused-import

    BERNARD_LEDIT_AVAILABLE = True
except ImportError:
    BERNARD_LEDIT_AVAILABLE = False


def requires_bernard() -> None:
    """Raises a clear error if Bernard L'Édit is not installed."""
    if not BERNARD_LEDIT_AVAILABLE:
        raise MindeeDependencyError(
            "This feature requires the 'Bernard L'Édit' library. "
            "Install it directly or run `pip install bernard-ledit` instead of `mindee-lite`."
        )
