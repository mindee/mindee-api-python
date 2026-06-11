from typing import ClassVar

from mindee.v2.client_options.base_parameters import BaseParameters


class ClassificationParameters(BaseParameters):
    """
    Parameters accepted by the classification utility v2 endpoint.
    """

    _slug: ClassVar[str] = "products/classification"
