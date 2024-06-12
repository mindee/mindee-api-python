from mindee.image_extraction.common import ExtractedImage
from mindee.input import LocalInputSource


class ExtractedMultiReceiptsImage(ExtractedImage):
    """Wrapper class for extracted multiple-receipts images."""

    def __init__(
        self,
        input_source: LocalInputSource,
        page_id: int,
        receipt_id: int,
    ):
        super().__init__(input_source, page_id, receipt_id)
        self._receipt_id = receipt_id

    @property
    def receipt_id(self):
        """
        ID of the receipt on a given page.

        :return:
        """
        return self._receipt_id
