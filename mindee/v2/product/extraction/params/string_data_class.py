import json
from dataclasses import asdict, dataclass


@dataclass
class StringDataClass:
    """Base class for dataclasses that can be serialized to JSON."""

    @staticmethod
    def _no_none_values(x) -> dict:
        """Don't include None values in the JSON output."""
        return {k: v for (k, v) in x if v is not None}

    def __str__(self) -> str:
        return json.dumps(
            asdict(self, dict_factory=self._no_none_values), indent=None, sort_keys=True
        )
