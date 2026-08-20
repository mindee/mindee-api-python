from typing import ClassVar

from mindee.v2.client_options.base_product_parameters import BaseProductParameters


class OCRParameters(BaseProductParameters):
    """
    Parameters accepted by the ocr utility v2 endpoint.
    """

    _slug: ClassVar[str] = "products/ocr"
