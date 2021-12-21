import requests

MINDEE_API_URL = "https://api.mindee.net/v1"


def make_api_url(endpoint: str, version: str, owner: str = "mindee"):
    """
    Returns full HTTP URL for a product at specific version
    :param endpoint: my_api
    :param version: 1
    :param owner: mindee
    :return: full URL, i.e. https://api.mindee.net/v1/products/mindee/invoices/2/predict
    """
    return (
        MINDEE_API_URL
        + "/products/"
        + owner
        + "/"
        + endpoint
        + "/"
        + version
        + "/predict"
    )


def make_api_request(url, input_file, token, include_words=False):
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

    response = requests.post(url, files=files, headers=headers, data=params)

    input_file.file_object.close()

    return response


class HTTPException(Exception):
    def __init__(self, message):
        self.message = message
