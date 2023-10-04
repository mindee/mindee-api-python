from typing import Optional

class Product:
    """Class for keeping track of a product's info."""
    name: Optional[str]
    version: Optional[str]

    def __init__(self, name=None, version=None) -> None:
        self.name = name
        self.version = version

    def __str__(self) -> str:
        return f"{self.name} v{self.version}"
