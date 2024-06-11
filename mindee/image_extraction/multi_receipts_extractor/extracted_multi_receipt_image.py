from mindee.image_extraction.common import ExtractedImage


class ExtractedMultiReceiptsImage(ExtractedImage):
    """Wrapper class for extracted multiple-receipts images."""

    _receipt_id: int

    def __init__(self, buffer, receipt_id: int, page_id: int):
        super().__init__(buffer, f"receipt_p{page_id}_{receipt_id}.pdf")
        self._receipt_id = receipt_id
        self._page_id = page_id

    @property
    def receipt_id(self):
        """
        ID of the receipt on a given page.

        :return:
        """
        return self._receipt_id

    @property
    def page_id(self):
        """
        ID of the page the receipt was found on.

        :return:
        """
        return self._page_id
