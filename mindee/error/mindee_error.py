class MindeeError(RuntimeError):
    """A generic exception relating to various HTTP errors."""


class MindeeClientError(MindeeError):
    """
    An exception relating to document parsing errors.

    Not to be confused with `MindeeHTTPClientError`.
    """


class MindeeApiError(MindeeError):
    """An exception relating to settings of the MindeeClient."""


class MindeeApiV2Error(MindeeError):
    """An exception relating to settings of the MindeeClient V2."""


class MindeeSourceError(MindeeError):
    """An exception relating to document loading."""


class MindeeProductError(MindeeApiError):
    """An exception relating to the use of an incorrect product/version."""
