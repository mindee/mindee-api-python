from typing import ClassVar

from mindee.v2.client_options.base_classification_product_parameters import (
    BaseClassificationProductParameters,
)


class CropParameters(BaseClassificationProductParameters):
    """Parameters for sending a file to a Crop product."""

    _slug: ClassVar[str] = "crop"
