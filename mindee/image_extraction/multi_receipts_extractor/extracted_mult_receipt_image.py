from mindee.image_extraction.common import ExtractedImage


class ExtractedMultiReceiptImage(ExtractedImage):
    _receipt_id: int
    page_id:  int

    def __init__(self, buffer, receipt_id: int, page_id: int):
        super().__init__(buffer, f"receipt_p{page_id}_{receipt_id}.pdf")
        self._receipt_id = receipt_id
        self._page_id = page_id

    @property
    def receipt_id(self):
        return self._receipt_id

    @property
    def page_id(self):
        return self.page_id
