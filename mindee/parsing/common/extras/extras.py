from abc import ABC

from mindee.parsing.common.string_dict import StringDict


class ExtraField(ABC):
    """Extra utilities."""


class Extras:
    """
    ExtraField collection wrapper class.

    Is roughly equivalent to a dict of Extras, with a bit more utility.
    """

    def __init__(self, raw_prediction: StringDict):
        for key, extra in raw_prediction.items():
            setattr(self, key, extra)

    def __str__(self) -> str:
        out_str = ""
        for attr in dir(self):
            if not attr.startswith("__"):
                out_str += f":{attr}: {getattr(self, attr).__str__()}\n"
        return out_str
