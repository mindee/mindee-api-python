from dataclasses import dataclass
from typing import Tuple


@dataclass
class PDFCharData:
    """Data class representing character data."""

    char: str
    """The character."""
    left: int
    """Left bound."""
    right: int
    """Right bound."""
    top: int
    """Top bound."""
    bottom: int
    """Bottom bound."""
    font_name: str
    """The font name."""
    font_size: float
    """The font size in pt."""
    font_weight: int
    """The font weight."""
    font_flags: int
    """The font flags."""
    font_stroke_color: Tuple[int, int, int, int]
    """RGBA representation of the font's stroke color."""
    font_fill_color: Tuple[int, int, int, int]
    """RGBA representation of the font's fill color."""
    page_id: int
    """ID of the page the character was found on."""
