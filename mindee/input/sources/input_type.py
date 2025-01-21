from enum import Enum


class InputType(Enum):
    """The input type, for internal use."""

    FILE = "file"
    BASE64 = "base64"
    BYTES = "bytes"
    PATH = "path"
    URL = "url"
