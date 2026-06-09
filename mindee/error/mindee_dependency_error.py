from mindee.error import MindeeError


class MindeeDependencyError(MindeeError, RuntimeError):
    """An exception relating to missing dependencies."""
