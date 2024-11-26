from typing import Optional

from mindee.parsing.common.string_dict import StringDict


class ExecutionFile:
    """Execution File class."""

    name: Optional[str]
    """File name."""

    alias: Optional[str]
    """File name."""

    def __init__(self, json_response: StringDict):
        self.name = json_response["name"]
        self.alias = json_response["alias"]
