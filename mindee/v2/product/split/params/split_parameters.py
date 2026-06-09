from typing import ClassVar

from mindee.v2.client_options.base_parameters import BaseParameters


class SplitParameters(BaseParameters):
    """
    Parameters accepted by the split utility v2 endpoint.
    """

    _slug: ClassVar[str] = "products/split"
