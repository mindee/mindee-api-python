from mindee.parsing.common.string_dict import StringDict


class ExecutionFile:
    """Execution File class."""

    name: str | None
    """File name."""

    alias: str | None
    """File name."""

    def __init__(self, raw_response: StringDict):
        self.name = raw_response["name"]
        self.alias = raw_response["alias"]
