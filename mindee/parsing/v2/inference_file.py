class InferenceFile:
    """Inference File info."""

    name: str
    """Name of the file."""
    alais: str
    """Alias of the file."""

    def __init__(self, json_response: dict) -> None:
        self.name = json_response["name"]
        self.alias = json_response["alias"]
