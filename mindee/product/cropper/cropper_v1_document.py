from typing import Optional

from mindee.parsing.common import Prediction, StringDict, clean_out_string


class CropperV1Document(Prediction):
    """Document data for Cropper, API version 1."""


    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Cropper document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """

    def __str__(self) -> str:
        return ""
