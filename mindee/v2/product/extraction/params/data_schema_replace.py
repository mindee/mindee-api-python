from dataclasses import dataclass
from typing import List, Union

from mindee.v2.product.extraction.params.data_schema_field import DataSchemaField
from mindee.v2.product.extraction.params.string_data_class import StringDataClass


@dataclass
class DataSchemaReplace(StringDataClass):
    """The structure to completely replace the data schema of the model."""

    fields: List[Union[DataSchemaField, dict]]

    def __post_init__(self) -> None:
        if not self.fields:
            raise ValueError("Data schema replacement fields cannot be empty.")
        if isinstance(self.fields[0], dict):
            self.fields = [
                DataSchemaField(**field)  # type: ignore[arg-type]
                for field in self.fields
            ]
