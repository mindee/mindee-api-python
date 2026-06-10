from mindee.error import MindeeError


class MindeeDependencyError(MindeeError, ImportError):
    """An exception relating to missing dependencies."""
