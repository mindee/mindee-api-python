from mindee.input.base_parameters import BaseParameters


class UtilityParameters(BaseParameters):
    """Parameters accepted by the utility v2 endpoint."""

    @classmethod
    def get_enqueue_slug(cls) -> str:
        return "utilities/" + cls._slug
