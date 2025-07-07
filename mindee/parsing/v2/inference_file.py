from mindee.parsing.common.string_dict import StringDict


class InferenceFile:
    """Inference File info."""

    name: str
    """Name of the file."""
    alais: str
    """Alias of the file."""

    def __init__(self, raw_response: StringDict) -> None:
        self.name = raw_response["name"]
        self.alias = raw_response["alias"]
