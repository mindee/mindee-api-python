from mindee.image_extraction.common import ExtractedImage


class ExtractedMultiReceiptsImage(ExtractedImage):
    """Wrapper class for extracted multiple-receipts images."""

    def __init__(self, buffer, file_name: str, receipt_id: int, page_id: int):
        super().__init__(buffer, file_name, page_id)
        self._receipt_id = receipt_id

    @property
    def receipt_id(self):
        """
        ID of the receipt on a given page.

        :return:
        """
        return self._receipt_id
