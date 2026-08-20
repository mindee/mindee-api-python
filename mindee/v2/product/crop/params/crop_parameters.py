from typing import ClassVar

from mindee.v2.client_options.base_product_parameters import BaseProductParameters


class CropParameters(BaseProductParameters):
    """
    Parameters accepted by the crop utility v2 endpoint.
    """

    _slug: ClassVar[str] = "products/crop"
