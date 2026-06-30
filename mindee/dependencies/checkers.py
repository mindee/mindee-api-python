from mindee.error.mindee_dependency_error import MindeeDependencyError

try:
    import PIL  # noqa: F401 #pylint: disable=unused-import

    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

try:
    import bernard_ledit  # noqa: F401 #pylint: disable=unused-import

    BERNARD_LEDIT_AVAILABLE = True
except ImportError:
    BERNARD_LEDIT_AVAILABLE = False


def require_pillow() -> None:
    """Raises a clear error if Pillow is not installed."""
    if not PILLOW_AVAILABLE:
        raise MindeeDependencyError(
            "This feature requires the 'Pillow' library. "
            "Install it directly or run `pip install mindee` instead of `mindee-lite`."
        )


def requires_bernard() -> None:
    """Raises a clear error if Bernard L'Édit is not installed."""
    if not BERNARD_LEDIT_AVAILABLE:
        raise MindeeDependencyError(
            "This feature requires the 'Bernard L'Édit' library. "
            "Install it directly or run `pip install bernard-ledit` instead of `mindee-lite`."
        )
