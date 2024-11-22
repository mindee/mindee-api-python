from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import FieldConfidenceMixin, FieldPositionMixin


class ResumeV1SocialNetworksUrl(FieldPositionMixin, FieldConfidenceMixin):
    """The list of social network profiles of the candidate."""

    name: Optional[str]
    """The name of the social network."""
    url: Optional[str]
    """The URL of the social network."""
    page_n: int
    """The document page on which the information was found."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        self._set_confidence(raw_prediction)
        self._set_position(raw_prediction)

        if page_id is None:
            try:
                self.page_n = raw_prediction["page_id"]
            except KeyError:
                pass
        else:
            self.page_n = page_id

        self.name = raw_prediction["name"]
        self.url = raw_prediction["url"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["name"] = format_for_display(self.name)
        out_dict["url"] = format_for_display(self.url)
        return out_dict

    def _table_printable_values(self) -> Dict[str, str]:
        """Return values for printing inside an RST table."""
        out_dict: Dict[str, str] = {}
        out_dict["name"] = format_for_display(self.name, 20)
        out_dict["url"] = format_for_display(self.url, 50)
        return out_dict

    def to_table_line(self) -> str:
        """Output in a format suitable for inclusion in an rST table."""
        printable = self._table_printable_values()
        out_str: str = f"| {printable['name']:<20} | "
        out_str += f"{printable['url']:<50} | "
        return clean_out_string(out_str)

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Name: {printable['name']}, \n"
        out_str += f"URL: {printable['url']}, \n"
        return clean_out_string(out_str)
