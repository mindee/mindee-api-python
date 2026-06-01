from mindee.v1.error.mindee_api_error import MindeeAPIError


class MindeeProductError(MindeeAPIError):
    """An exception relating to the use of an incorrect product/version."""
