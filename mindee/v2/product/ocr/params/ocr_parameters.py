from typing import ClassVar

from mindee.v2.client_options.base_product_parameters import BaseProductParameters


class OCRParameters(BaseProductParameters):
    """Parameters for sending a file to a Raw Text (OCR) product."""

    _slug: ClassVar[str] = "ocr"
