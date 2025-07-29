from mindee.parsing.common.string_dict import StringDict


class InferenceFile:
    """Inference File info."""

    name: str
    """Name of the file."""
    alias: str
    """Alias of the file."""
    page_count: str
    """Number of pages in the file."""
    mime_type: str
    """Mime type of the file."""

    def __init__(self, raw_response: StringDict) -> None:
        self.name = raw_response["name"]
        self.alias = raw_response["alias"]
        self.page_count = raw_response["page_count"]
        self.mime_type = raw_response["mime_type"]

    def __str__(self) -> str:
        return (
            f"File\n===="
            f"\n:Name: {self.name}"
            f"\n:Alias:{self.alias if self.alias else ''}"
            f"\n:Page Count: {self.page_count}"
            f"\n:MIME Type: {self.mime_type}"
        )
