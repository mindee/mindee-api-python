import requests
from mindee.versions import __version__, python_version, get_platform

MINDEE_API_URL = "https://api.mindee.net/v1"

PLATFORM = get_platform()


def make_predict_url(product: str, version: str, owner: str = "mindee") -> str:
    """
    Returns full HTTP URL for a prediction request at specific version
    :param product: product API name
    :param version: product model version
    :param owner: product owner (mindee for off-the-shelf APIs)
    :return: The full URL, i.e. https://api.mindee.net/v1/products/mindee/invoices/2/predict
    """
    return f"{MINDEE_API_URL}/products/{owner}/{product}/v{version}/predict"


def make_api_request(url: str, input_file, token: str, include_words: bool = False):
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
        "User-Agent": f"mindee-api-python@v{__version__} python-v{python_version} {PLATFORM}",
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
