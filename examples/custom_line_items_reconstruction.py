import os

from mindee import Client, product
from mindee.parsing.common.predict_response import PredictResponse

CUSTOM_ENDPOINT_NAME = os.getenv("CUSTOM_ENDPOINT_NAME", "my-endpoint-name")
CUSTOM_ACCOUNT_NAME = os.getenv("CUSTOM_ACCOUNT_NAME", "my-account-name")
CUSTOM_VERSION = os.getenv("CUSTOM_VERSION", "1")
CUSTOM_DOCUMENT_PATH = os.getenv("CUSTOM_DOCUMENT_PATH", "path/to/your/file.ext")

# This example assumes you are following the associated tutorial:
# https://developers.mindee.com/docs/extracting-line-items-tutorial#line-reconstruction-code
anchors = ["category"]
columns = ["category", "previous_year_actual", "year_actual", "year_projection"]


def get_field_content(line, field) -> str:
    if field in line.fields:
        return str(line.fields[field].content)
    return ""


def print_line(line) -> None:
    category = get_field_content(line, "category")
    previous_year_actual = get_field_content(line, "previous_year_actual")
    year_actual = get_field_content(line, "year_actual")
    year_projection = get_field_content(line, "year_projection")
    # here ljust() fills the rest of the given size with spaces
    string_line = (
        category.ljust(20, " ")
        + previous_year_actual.ljust(10, " ")
        + year_projection.ljust(10, " ")
        + year_actual
    )

    print(string_line)


client = Client()

custom_endpoint = client.create_endpoint(
    CUSTOM_ENDPOINT_NAME, CUSTOM_ACCOUNT_NAME, CUSTOM_VERSION
)
input_doc = client.source_from_path(CUSTOM_DOCUMENT_PATH)


response: PredictResponse[product.CustomV1] = client.parse(
    product.CustomV1, input_doc, endpoint=custom_endpoint
)
line_items = response.document.inference.prediction.columns_to_line_items(
    anchors, columns
)

for line in line_items:
    print_line(line)
