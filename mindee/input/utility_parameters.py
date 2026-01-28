from dataclasses import dataclass

from mindee.input.base_parameters import BaseParameters


@dataclass
class UtilityParameters(BaseParameters):
    """
    Parameters accepted by any of the asynchronous **inference** utility v2 endpoints.
    """
