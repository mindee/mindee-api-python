from typing import Optional

from mindee.parsing.common.string_dict import StringDict


class ExecutionFile:
    """Execution File class."""

    name: Optional[str]
    """File name."""

    alias: Optional[str]
    """File name."""

    def __init__(self, raw_response: StringDict):
        self.name = raw_response["name"]
        self.alias = raw_response["alias"]
