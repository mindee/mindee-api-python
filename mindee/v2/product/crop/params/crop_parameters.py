from typing import ClassVar

from mindee.v2.client_options.base_product_parameters import BaseProductParameters


class CropParameters(BaseProductParameters):
    """Parameters for sending a file to a Crop product."""

    _slug: ClassVar[str] = "crop"
