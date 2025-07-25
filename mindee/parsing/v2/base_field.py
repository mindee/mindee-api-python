from typing import List, Optional

from mindee.parsing.v2.dynamic_field import DynamicField


class BaseField(DynamicField):
    """Field with base information."""

    locations: List
    confidence: Optional[str]
