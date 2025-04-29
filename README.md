[![License: MIT](https://img.shields.io/github/license/mindee/mindee-api-python)](https://opensource.org/licenses/MIT) [![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/mindee/mindee-api-python/unit-test.yml)](https://github.com/mindee/mindee-api-python) [![PyPI Version](https://img.shields.io/pypi/v/mindee)](https://pypi.org/project/mindee/) [![versions](https://img.shields.io/pypi/pyversions/mindee.svg)](https://github.com/mindee/mindee-api-python) [![Downloads](https://img.shields.io/pypi/dm/mindee)](https://pypi.org/project/mindee/)

# Mindee API Helper Library for Python
Quickly and easily connect to Mindee's API services using Python.

## Quick Start
Here's the TL;DR of getting started.

First, get an [API Key](https://developers.mindee.com/docs/create-api-key)

Then, install this library:
```shell
pip install mindee
```

Finally, Python away!

### Loading a File and Parsing It

#### Global Documents
```python
from mindee import Client, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Parse the document as an invoice by passing the appropriate type
result = mindee_client.parse(product.InvoiceV4, input_doc)

# Print a brief summary of the parsed data
print(result.document)
```

**Note:** Files can also be loaded from:

A python `BinaryIO` compatible file:
```python
input_doc = mindee_client.source_from_file(my_file)
```

A URL (`HTTPS` only):
```python
input_doc = mindee_client.source_from_url(
    "https://files.readme.io/a74eaa5-c8e283b-sample_invoice.jpeg"
)
```

A base64-encoded string, making sure to specify the extension of the file name:
```python
input_doc = mindee_client.source_from_b64string(
    my_input_string, "my-file-name.ext"
)
```

Raw bytes, making sure to specify the extension of the file name:
```python
input_doc = mindee_client.source_from_bytes(
    my_raw_bytes_sequence, "my-file-name.ext"
)
```

#### Region-Specific Documents
```python
from mindee import Client, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Parse the document as a USA bank check by passing the appropriate type
result = mindee_client.parse(product.us.BankCheckV1, input_doc)

# Print a brief summary of the parsed data
print(result.document)
```

#### Custom Documents (docTI & Custom APIs)

```python
from mindee import Client, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Add your custom endpoint (document)
my_endpoint = mindee_client.create_endpoint(
    account_name="my-account",
    endpoint_name="my-endpoint",
)

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Parse the file.
# The endpoint must be specified since it cannot be determined from the class.
result = mindee_client.enqueue_and_parse(
    product.GeneratedV1,
    input_doc,
    endpoint=my_endpoint
)

# Print a brief summary of the parsed data
print(result.document)

# Iterate over all the fields in the document
for field_name, field_values in result.document.fields.items():
    print(field_name, "=", field_values)
```

### Enqueue and Parse a Webhook Response
This is an optional way of handling asynchronous APIs.

```python
from mindee import Client, product

mindee_client = Client()
input_source = mindee_client.source_from_path("/path/to/the/file.ext")

result = mindee_client.enqueue_and_parse(
    product.FinancialDocumentV1,
    input_source,
    workflow_id="my-workflow-id",
    rag=True,
)

print(result.document)
```

### Additional Options
Options to pass when sending a file.
```python
from mindee import Client, product
from mindee.client import LocalResponse

mindee_client = Client()
input_source = mindee_client.source_from_path("/path/to/the/file.ext")

enqueue_response = mindee_client.enqueue(
    product.InternationalIdV2,
    input_source,
)

# You can keep track of the job's ID for traceability concerns.
job_id = enqueue_response.job.id


# Load the JSON string sent by the Mindee webhook POST callback.
# Reading the callback data will vary greatly depending on your HTTP server.
# This is therefore beyond the scope of this example.

local_response = LocalResponse(request.body())

# You can also load the json from a local path.
# local_response = LocalResponse("path/to/my/file.ext")

# Optional: verify the HMAC signature
# You'll need to get the "X-Mindee-Hmac-Signature" custom HTTP header.
hmac_signature = request.headers.get("X-Mindee-Hmac-Signature")
if not local_response.is_valid_hmac_signature(my_secret_key, hmac_signature):
    raise Error("Bad HMAC signature! Is someone trying to do evil?")

# Deserialize the response

result = mindee_client.load_prediction(
    product.InternationalIdV2,
    local_response
)

# Print a full summary of the parsed data in RST format
print(result.document)
```


#### Page Options
Allows sending only certain pages in a PDF.

In this example we only send the first, penultimate and last pages:

```python
from mindee import product, PageOptions

result = mindee_client.parse(
    product.InvoiceV4,
    input_source,
    page_options=PageOptions(
        page_indexes=[0, -2, -1],
        operation=PageOptions.KEEP_ONLY,
        on_min_pages=2
    )
)
```

## Further Reading
Complete details on the working of the library are available in the following guides:

* [Getting started](https://developers.mindee.com/docs/python-getting-started)
* [Python Command Line Interface (CLI)](https://developers.mindee.com/docs/python-cli)
* [Python Generated](https://developers.mindee.com/docs/generated-api-python)
* [Python Custom APIs (Deprecated - API Builder)](https://developers.mindee.com/docs/python-api-builder)
* [Python Invoice OCR](https://developers.mindee.com/docs/python-invoice-ocr)
* [Python International Id OCR](https://developers.mindee.com/docs/python-international-id-ocr)
* [Python Resume OCR](https://developers.mindee.com/docs/python-resume-ocr)
* [Python Receipt OCR](https://developers.mindee.com/docs/python-receipt-ocr)
* [Python Financial Document OCR](https://developers.mindee.com/docs/python-financial-document-ocr)
* [Python Passport OCR](https://developers.mindee.com/docs/python-passport-ocr)
* [Python Proof of Address OCR](https://developers.mindee.com/docs/python-proof-of-address-ocr)
* [Python US Driver License OCR](https://developers.mindee.com/docs/python-eu-driver-license-ocr)
* [Python FR Bank Account Detail OCR](https://developers.mindee.com/docs/python-fr-bank-account-details-ocr)
* [Python FR Carte Grise OCR](https://developers.mindee.com/docs/python-fr-carte-grise-ocr)
* [Python FR Health Card OCR](https://developers.mindee.com/docs/python-fr-health-card-ocr)
* [Python FR ID Card OCR](https://developers.mindee.com/docs/python-fr-carte-nationale-didentite-ocr)
* [Python US Bank Check OCR](https://developers.mindee.com/docs/python-us-bank-check-ocr)
* [Python US W9 OCR](https://developers.mindee.com/docs/python-us-w9-ocr)
* [Python Barcode Reader API](https://developers.mindee.com/docs/python-barcode-reader-ocr)
* [Python Cropper API](https://developers.mindee.com/docs/python-cropper-ocr)
* [Python Invoice Splitter API](https://developers.mindee.com/docs/python-invoice-splitter-api)
* [Python Multi Receipts Detector API](https://developers.mindee.com/docs/python-multi-receipts-detector-ocr)

You can view the source code on [GitHub](https://github.com/mindee/mindee-api-python).

You can also take a look at the
**[Reference Documentation](https://mindee.github.io/mindee-api-python/)**.

## License
Copyright © Mindee

Available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).

## Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
