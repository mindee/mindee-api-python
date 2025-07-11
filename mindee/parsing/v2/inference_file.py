from typing import Optional

from mindee.parsing.common.string_dict import StringDict


class InferenceFile:
    """Inference File info."""

    name: str
    """Name of the file."""
    alias: Optional[str]
    """Alias of the file."""

    def __init__(self, raw_response: StringDict) -> None:
        self.name = raw_response["name"]
        self.alias = raw_response["alias"]

    def __str__(self, indent: int = 0) -> str:
        return (
            f"{'  ' * indent}:name: {self.name}\n"
            f"{'  ' * indent}:alias: {self.alias if self.alias else ''}\n"
        )
