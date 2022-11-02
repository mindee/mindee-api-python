from typing import NamedTuple, Sequence

KEEP_ONLY = "KEEP_ONLY"
REMOVE = "REMOVE"


class PageOptions(NamedTuple):
    page_indexes: Sequence[int]
    """
    Zero-based list of page indexes.
    A negative index can be used, indicating an offset from the end of the document.

    `[0, -1]` represents the fist and last pages of the document.
    """
    operation: str = KEEP_ONLY
    """
    Operation to apply on the document, given the ``page_indexes`` specified:

    * ``KEEP_ONLY`` - keep only the specified pages, and remove all others.
    * ``REMOVE`` - remove the specified pages, and keep all others.
    """
    on_min_pages: int = 0
    """
    Apply the operation only if document has at least this many pages.

    Default: `0` (apply on all documents)
    """
