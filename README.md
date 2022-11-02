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

### Off-the-Shelf Documents
World-wide documents:
```python
from mindee import Client, documents

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.doc_from_path("/path/to/the/invoice.pdf")
# Parse the document as an invoice by passing the appropriate type
api_response = input_doc.parse(documents.TypeInvoiceV3)

# Print a brief summary of the parsed data
print(api_response.document)
```

Region-specific documents:
```python
from mindee import Client, documents

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.doc_from_path("/path/to/the/check.jpg")
# Parse the document as a USA bank check by passing the appropriate type
api_response = input_doc.parse(documents.us.TypeBankCheckV1)

# Print a brief summary of the parsed data
print(api_response.document)
```

### Custom Document (API Builder)

```python
from mindee import Client, documents

# Init a new client and add your custom endpoint (document)
mindee_client = Client(api_key="my-api-key").add_endpoint(
    account_name="john",
    endpoint_name="wnine",
)

# Load a file from disk and parse it.
# The endpoint name must be specified since it can't be determined from the class.
api_response = mindee_client.doc_from_path(
    "/path/to/the/w9.jpg"
).parse(documents.TypeCustomV1, endpoint_name="wnine")

# Print a brief summary of the parsed data
print(api_response.document)
```

## Further Reading
There's more to it than that for those that need more features, or want to
customize the experience.

All the juicy details are described in the
**[Official Guide](https://developers.mindee.com/docs/python-sdk)**.

You can also take a look at the
**[Reference Documentation](https://mindee.github.io/mindee-api-python/)**.

## License
Copyright © Mindee

Available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).
