class PaginationMetadata:
    """Pagination metadata."""

    per_page: int
    """Number of results per page."""
    page: int
    """1-indexed page number."""
    total_items: int
    """Total number of items."""
    total_pages: int
    """Total number of pages."""
    total_items_unfiltered: int | None
    """Total number of items, including unfiltered results."""

    def __init__(self, server_response: dict) -> None:
        self.per_page = server_response["per_page"]
        self.page = server_response["page"]
        self.total_items = server_response["total_items"]
        self.total_pages = server_response["total_pages"]
        self.total_items_unfiltered = server_response.get("total_items_unfiltered")

    def __str__(self) -> str:
        return (
            f":Per Page: {self.per_page}\n"
            f":Page: {self.page}\n"
            f":Total Items: {self.total_items}\n"
            f":Total Pages: {self.total_pages}\n"
        )
