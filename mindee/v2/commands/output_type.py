from enum import Enum


class OutputType(str, Enum):
    """How to output the response from a V2 inference command."""

    SUMMARY = "summary"
    """Document-level summary in rST format (default)."""
    FULL = "full"
    """Complete response in rST format, including active options."""
    RAW = "raw"
    """Raw JSON response."""
