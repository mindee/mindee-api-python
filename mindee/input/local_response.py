import hashlib
import hmac
import io
import json
import os
from pathlib import Path
from typing import Any, BinaryIO, Dict, Union

from mindee.error.mindee_error import MindeeError


class LocalResponse:
    """Local response loaded from a file."""

    _file: BinaryIO
    """File object of the local response."""

    def __init__(self, input_file: Union[BinaryIO, str, Path, bytes]):
        if isinstance(input_file, (BinaryIO, io.BufferedReader)):
            str_stripped = (
                input_file.read().decode("utf-8").replace("\r", "").replace("\n", "")
            )
            self._file = io.BytesIO(str_stripped.encode("utf-8"))
            self._file.seek(0)
        elif isinstance(input_file, Path) or (
            isinstance(input_file, str) and os.path.exists(input_file)
        ):
            with open(input_file, "r", encoding="utf-8") as file:
                self._file = io.BytesIO(
                    file.read().replace("\r", "").replace("\n", "").encode()
                )
        elif isinstance(input_file, str):
            self._file = io.BytesIO(
                input_file.replace("\r", "").replace("\n", "").encode("utf-8")
            )
        elif isinstance(input_file, bytes):
            str_stripped = (
                input_file.decode("utf-8").replace("\r", "").replace("\n", "")
            )
            self._file = io.BytesIO(str_stripped.encode("utf-8"))
            self._file.seek(0)
        else:
            raise MindeeError(f"Incompatible type for input '{type(input_file)}'.")

    @property
    def as_dict(self) -> Dict[str, Any]:
        """
        Returns the dictionary representation of the file.

        :return: A json-like dictionary.
        """
        try:
            self._file.seek(0)
            out_json = json.loads(self._file.read())
        except json.decoder.JSONDecodeError as exc:
            raise MindeeError("File is not a valid dictionary.") from exc
        return out_json

    @staticmethod
    def _process_secret_key(
        secret_key: Union[str, bytes, bytearray],
    ) -> Union[bytes, bytearray]:
        """
        Processes the secret key as a byte array.

        :param secret_key: Secret key, either a string or a byte/byte array.
        :return: a byte/byte array secret key.
        """
        if isinstance(secret_key, (bytes, bytearray)):
            return secret_key
        return secret_key.encode("utf-8")

    def get_hmac_signature(self, secret_key: Union[str, bytes, bytearray]):
        """
        Returns the hmac signature of the local response, from the secret key provided.

        :param secret_key: Secret key, either a string or a byte/byte array.
        :return: The hmac signature of the local response.
        """
        algorithm = hashlib.sha256

        try:
            self._file.seek(0)
            mac = hmac.new(
                LocalResponse._process_secret_key(secret_key),
                self._file.read(),
                algorithm,
            )
        except (TypeError, ValueError) as exc:
            raise MindeeError("Could not get HMAC signature from payload.") from exc

        return mac.hexdigest()

    def is_valid_hmac_signature(
        self, secret_key: Union[str, bytes, bytearray], signature: str
    ):
        """
        Checks if the hmac signature of the local response is valid.

        :param secret_key: Secret key, given as a string.
        :param signature: HMAC signature, given as a string.
        :return: True if the HMAC signature is valid.
        """
        return signature == self.get_hmac_signature(secret_key)
