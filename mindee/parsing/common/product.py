from mindee.parsing.common.string_dict import StringDict


class Product:
    """Class for keeping track of a product's info."""

    name: str
    version: str

    def __init__(self, raw_prediction: StringDict) -> None:
        self.name = raw_prediction["name"]
        self.version = raw_prediction["version"]

    def __str__(self) -> str:
        return f"{self.name} v{self.version}"
