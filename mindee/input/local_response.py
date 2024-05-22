import json
from pathlib import Path
from typing import Union, BinaryIO, Dict, Any
import io

from mindee.error import MindeeError


class LocalResponse:
    json: Dict[str, Any]

    def __init__(self, input_file: Union[BinaryIO, str, Path, bytes]):
        input_binary: BinaryIO
        if isinstance(input_file, BinaryIO):
            input_binary = input_file
            input_binary.seek(0)
        elif isinstance(input_file, str) or isinstance(input_file, Path):
            with open(input_file, 'rb') as f:
                input_binary = io.BytesIO(f.read())
        elif isinstance(input_file, bytes):
            input_binary = io.BytesIO(input_file)
        else:
            raise TypeError('Incompatible type for input.')
        try:
            input_binary.seek(0)
            self.json = json.load(input_binary)
            input_binary.close()
        except json.decoder.JSONDecodeError as exc:
            raise MindeeError('File is not a valid dictionary.') from exc
