import json
from dataclasses import dataclass

from mindee.v2.product.extraction.params.data_schema_replace import DataSchemaReplace
from mindee.v2.product.extraction.params.string_data_class import StringDataClass


@dataclass
class DataSchema(StringDataClass):
    """Modify the Data Schema."""

    replace: DataSchemaReplace | dict | str | None = None
    """If set, completely replaces the data schema of the model."""

    def __post_init__(self) -> None:
        if isinstance(self.replace, dict):
            self.replace = DataSchemaReplace(**self.replace)
        elif isinstance(self.replace, str):
            self.replace = DataSchemaReplace(**json.loads(self.replace))
