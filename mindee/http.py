import requests
from mindee.versions import __version__, python_version, get_platform

platform = get_platform()


def request(url, input_file, token, include_words=False):
    """
    :param input_file: Input object
    :param url: Endpoint url
    :param token: X-Inferuser-Token
    :param include_words: Include Mindee vision words in http_response
    :return: requests response
    """
    input_file.file_object.seek(0)

    files = {"document": (input_file.filename, input_file.file_object.read())}
    headers = {
        "Authorization": f"Token {token}",
        "User-Agent": f"mindee-api-python@v{__version__} python-v{python_version} {platform}",
    }

    params = {}
    if include_words:
        params["include_mvision"] = "true"

    response = requests.post(url, files=files, headers=headers, data=params)

    input_file.file_object.close()

    return response


class HTTPException(Exception):
    def __init__(self, message):
        self.message = message
