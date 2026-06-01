from enum import Enum


class FieldConfidence(str, Enum):
    """Confidence level of a field as returned by the V2 API."""

    CERTAIN = "Certain"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

    def __int__(self) -> int:
        return {"Certain": 4, "High": 3, "Medium": 2, "Low": 1}[self.value]

    def __str__(self) -> str:
        return self.value

    def __lt__(self, other) -> bool:
        if isinstance(other, FieldConfidence):
            return int(self) < int(other)
        raise TypeError(f"Cannot compare FieldConfidence with {type(other)}")

    def __le__(self, other) -> bool:
        if isinstance(other, FieldConfidence):
            return int(self) <= int(other)
        raise TypeError(f"Cannot compare FieldConfidence with {type(other)}")

    def __gt__(self, other) -> bool:
        if isinstance(other, FieldConfidence):
            return int(self) > int(other)
        raise TypeError(f"Cannot compare FieldConfidence with {type(other)}")

    def __ge__(self, other) -> bool:
        if isinstance(other, FieldConfidence):
            return int(self) >= int(other)
        raise TypeError(f"Cannot compare FieldConfidence with {type(other)}")
