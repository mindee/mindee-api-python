from typing import NamedTuple, Sequence

KEEP_ONLY = "keep_only"
REMOVE = "remove"


class PageOptions(NamedTuple):
    page_indexes: Sequence
    """page numbers (indexes), 0 is the first page"""
    behavior: str = KEEP_ONLY
    """`keep_only` or `remove`"""
    on_min_pages: int = 5
    """Apply the operation only if document has at least this many pages."""
