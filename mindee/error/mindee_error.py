class MindeeError(RuntimeError):
    """A generic exception relating to various HTTP errors."""


class MindeeClientError(MindeeError):
    """
    An exception relating to document parsing errors.

    Not to be confused with `MindeeHTTPClientError`.
    """


class MindeeApiError(MindeeError):
    """An exception relating to settings of the MindeeClient."""


class MindeeSourceError(MindeeError):
    """An exception relating to document loading."""
