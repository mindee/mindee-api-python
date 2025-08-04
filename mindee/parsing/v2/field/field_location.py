from typing import Optional

from mindee.geometry import Polygon
from mindee.parsing.common.string_dict import StringDict


class FieldLocation:
    """Location of a field."""

    def __init__(self, server_response: StringDict) -> None:
        """
        Initialize FieldLocation from server response.

        :param server_response: Raw server response.
        """
        self.polygon: Optional[Polygon] = None
        self.page: Optional[int] = None

        if "polygon" in server_response and server_response["polygon"] is not None:
            self.polygon = Polygon(server_response["polygon"])

        if "page" in server_response and isinstance(server_response["page"], int):
            self.page = server_response["page"]

    def __str__(self) -> str:
        """
        String representation.

        :return: String representation of the field location.
        """
        return str(self.polygon) if self.polygon else ""
