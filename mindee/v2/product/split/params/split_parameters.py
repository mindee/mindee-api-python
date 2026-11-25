from typing import ClassVar

from mindee.v2.client_options.base_classification_product_parameters import (
    BaseClassificationProductParameters,
)


class SplitParameters(BaseClassificationProductParameters):
    """
    Parameters accepted by the split utility v2 endpoint.
    """

    _slug: ClassVar[str] = "split"
