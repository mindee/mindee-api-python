class PaginationMetadata:
    """Pagination metadata associated with searches."""

    per_page: int
    """Number of items per page."""
    page: int
    """1-indexed page number."""
    total_items: int
    """Total items."""
    total_pages: int
    """Total number of pages."""

    def __init__(self, server_response: dict) -> None:
        self.per_page = server_response["per_page"]
        self.page = server_response["page"]
        self.total_items = server_response["total_items"]
        self.total_pages = server_response["total_pages"]

    def __str__(self) -> str:
        """String representation of the pagination metadata."""
        return (
            f":Per Page: {self.per_page}\n"
            f":Page: {self.page}\n"
            f":Total Items: {self.total_items}\n"
            f":Total Pages: {self.total_pages}\n"
        )
