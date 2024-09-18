import re
from typing import List, Optional


def line_separator(column_sizes: List[int], separator: str) -> str:
    """Adds custom separators for console display in line-items-like fields."""
    out_str = "  +"
    for size in column_sizes:
        out_str += size * separator + "+"
    return out_str


def clean_out_string(out_string: str) -> str:
    """Clean up the string representation."""
    regexp = re.compile(r" \n")
    return regexp.sub("\n", out_string).strip()


def format_for_display(
    out_string: Optional[str] = None, max_col_size: Optional[int] = None
) -> str:
    """Truncates line-items to the max width of their corresponding column."""
    if not out_string or len(out_string) == 0:
        return ""
    out_string = (
        out_string.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    )
    if max_col_size is None:
        return out_string
    return (
        out_string
        if len(out_string) <= max_col_size
        else f"{out_string[:max_col_size-3]}..."
    )
