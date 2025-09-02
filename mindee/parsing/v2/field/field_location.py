from mindee.geometry.polygon import Polygon
from mindee.parsing.common.string_dict import StringDict


class FieldLocation:
    """Location of a field."""

    polygon: Polygon
    page: int

    def __init__(self, server_response: StringDict) -> None:
        """
        Initialize FieldLocation from server response.

        :param server_response: Raw server response.
        """
        self.polygon = Polygon(server_response["polygon"])
        self.page = int(server_response["page"])

    def __str__(self) -> str:
        """
        String representation.

        :return: String representation of the field location.
        """
        return f"{self.polygon} on page {self.page}"
