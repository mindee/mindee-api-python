[![License: MIT](https://img.shields.io/github/license/mindee/mindee-api-python)](https://opensource.org/licenses/MIT) [![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/mindee/mindee-api-python/test.yml)](https://github.com/mindee/mindee-api-python) [![PyPI Version](https://img.shields.io/pypi/v/mindee)](https://pypi.org/project/mindee/) [![Downloads](https://img.shields.io/pypi/dm/mindee)](https://pypi.org/project/mindee/)

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
from mindee import Client, documents

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.doc_from_path("/path/to/the/file.ext")

# Parse the document as an invoice by passing the appropriate type
result = input_doc.parse(documents.TypeInvoiceV4)

# Print a brief summary of the parsed data
print(result.document)
```

#### Region-Specific Documents
```python
from mindee import Client, documents

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.doc_from_path("/path/to/the/file.ext")

# Parse the document as a USA bank check by passing the appropriate type
result = input_doc.parse(documents.us.TypeBankCheckV1)

# Print a brief summary of the parsed data
print(result.document)
```

#### Custom Document (API Builder)

```python
from mindee import Client, documents

# Init a new client and add your custom endpoint (document)
mindee_client = Client(api_key="my-api-key").add_endpoint(
    account_name="john",
    endpoint_name="wnine",
)

# Load a file from disk and parse it.
# The endpoint name must be specified since it can't be determined from the class.
result = mindee_client.doc_from_path(
    "/path/to/the/file.ext"
).parse(documents.TypeCustomV1, endpoint_name="wnine")

# Print a brief summary of the parsed data
print(result.document)

# Iterate over all the fields in the document
for field_name, field_values in result.document.fields.items():
    print(field_name, "=", field_values)
```

## Further Reading
Complete details on the working of the library are available in the following guides:

* [Getting started](https://developers.mindee.com/docs/getting-started)
* [Command Line Interface (CLI)](https://developers.mindee.com/docs/python-cli)
* [Custom APIs (API Builder)](https://developers.mindee.com/docs/python-api-builder)
* [Invoice API](https://developers.mindee.com/docs/python-invoice-ocr)
* [Passport API](https://developers.mindee.com/docs/python-passport-ocr)
* [Receipt API](https://developers.mindee.com/docs/python-receipt-ocr)

You can view the source code on [GitHub](https://github.com/mindee/mindee-api-python).

You can also take a look at the
**[Reference Documentation](https://mindee.github.io/mindee-api-python/)**.

## License
Copyright © Mindee

Available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).

## Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-1jv6nawjq-FDgFcF2T5CmMmRpl9LLptw)
