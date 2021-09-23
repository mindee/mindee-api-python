import requests


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
    headers = {"Authorization": f"Token {token}"}

    params = {}
    if include_words:
        params["include_mvision"] = "true"

    response = requests.post(
        url,
        files=files,
        headers=headers,
        data=params
    )

    input_file.file_object.close()

    return response


class HTTPException(Exception):
    def __init__(self, message):
        self.message = message
