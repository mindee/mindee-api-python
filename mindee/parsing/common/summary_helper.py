import re
from typing import List


def line_separator(column_sizes: List[int], separator: str) -> str:
    """Adds custom separators for console display in line-items-like fields."""
    out_str = "  +"
    for size in column_sizes:
        out_str += size * separator + "+"
    return out_str


def clean_out_string(out_string: str) -> str:
    """Clean up the string representation."""
    regexp = re.compile(r" \n")
    return regexp.sub("\n", out_string)
