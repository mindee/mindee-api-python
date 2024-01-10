from typing import Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.custom.generated_list import GeneratedListField
from mindee.parsing.standard.base import BaseField
from mindee.parsing.standard.text import StringField


class GeneratedObjectField(BaseField):
    """A JSON-like object, with miscellaneous values."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ) -> None:
        for name, value in raw_prediction.items():
            item_page_id = page_id
            if isinstance(value, dict):
                if "page_id" in value and value["page_id"].isdigit():
                    item_page_id = int(value["page_id"])
                setattr(self, name, GeneratedObjectField(value, item_page_id))
            elif isinstance(value, list):
                setattr(self, name, GeneratedListField(value, item_page_id))
            else:
                setattr(self, name, StringField(value, page_id=item_page_id))

    def __str__(self, level=0) -> str:
        """
        String representation.

        Takes into account level of indentation.

        :param level: level of indent (times 2 spaces).
        """
        indent = "  " * level
        out_str = ""
        for name in dir(self):
            value = self.__getattribute__(name)
            if isinstance(value, GeneratedObjectField):
                out_str += f"\n{indent}:{name}:\n{indent}{value.__str__(level+1)}"
            elif isinstance(value, GeneratedListField):
                out_str += f"\n:{indent}{name}:\n{indent}{value}"
            else:
                out_str += f"\n:{indent}{name}: {value}"
        return clean_out_string(out_str)
