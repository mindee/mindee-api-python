from mindee.v2.parsing.inference.base_response import BaseResponse


class UtilityResponse(BaseResponse):
    """Base class for utility responses."""

    @classmethod
    def get_result_slug(cls) -> str:
        return "utilities/" + cls._slug
