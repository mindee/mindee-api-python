from typing import ClassVar

from mindee.v2.client_options.base_product_parameters import BaseProductParameters


class SplitParameters(BaseProductParameters):
    """
    Parameters accepted by the split utility v2 endpoint.
    """

    _slug: ClassVar[str] = "split"
