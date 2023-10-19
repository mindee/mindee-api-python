class MindeeError(RuntimeError):
    """A generic exception relating to various client errors."""


class MindeeClientError(MindeeError):
    """An exception relating to document parsing."""


class MindeeApiError(MindeeError):
    """An exception relating to settings of the MindeeClient."""


class MindeeSourceError(MindeeError):
    """An exception relating to document loading."""
