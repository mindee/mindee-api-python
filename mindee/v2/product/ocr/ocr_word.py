from mindee.geometry.polygon import Polygon


class OCRWord:
    """OCR result for a single word extracted from the document page."""

    content: str
    """Text content of the word."""
    polygon: Polygon
    """Position information as a list of points in clockwise order."""

    def __init__(self, raw_response: dict):
        self.content = raw_response["content"]
        self.polygon = Polygon(raw_response["polygon"])

    def __str__(self) -> str:
        return self.content
