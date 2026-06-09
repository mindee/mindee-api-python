from mindee.error.mindee_dependency_error import MindeeDependencyError

try:
    from PIL import Image  # noqa: F401 #pylint: disable=unused-import

    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

try:
    import pypdfium2  # noqa: F401 #pylint: disable=unused-import

    PYPDFIUM2_AVAILABLE = True
except ImportError:
    PYPDFIUM2_AVAILABLE = False


def require_pillow() -> None:
    """Raises a clear error if Pillow is not installed."""
    if not PILLOW_AVAILABLE:
        raise MindeeDependencyError(
            "This feature requires the 'Pillow' library. "
            "Install it directly or run `pip install mindee` instead of `mindee-lite`."
        )


def require_pypdfium2() -> None:
    """Raises a clear error if PyPDFium2 is not installed."""
    if not PYPDFIUM2_AVAILABLE:
        raise MindeeDependencyError(
            "This feature requires the 'PyPDFium2' library. "
            "Install it directly or run `pip install mindee` instead of `mindee-lite`."
        )
