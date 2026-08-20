from typing import ClassVar

from mindee.v2.client_options.base_product_parameters import BaseProductParameters


class ClassificationParameters(BaseProductParameters):
    """Parameters for sending a file to a Classification product."""

    _slug: ClassVar[str] = "classification"
