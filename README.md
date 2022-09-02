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

### Off-the-Shelf Document
```python
from mindee import Client

# Init a new client and configure the Invoice API
mindee_client = Client().config_invoice("my-api-key")

# Load a file from disk and parse it
api_response = mindee_client.doc_from_path("/path/to/the/invoice.pdf").parse("invoice")

# Print a brief summary of the parsed data
print(api_response.document)
```

### Custom Document (API Builder)
```python
from mindee import Client

# Init a new client and configure your custom document
mindee_client = Client().config_custom_doc(
    account_name="john",
    document_type="wnine",
    api_key="my-api-key"
)

# Load a file from disk and parse it
api_response = mindee_client.doc_from_path("/path/to/the/card.jpg").parse("wnine")

# Print a brief summary of the parsed data
print(api_response.document)
```

## Further Reading
There's more to it than that for those that need more features, or want to
customize the experience.

All the juicy details are described in the
**[Official Documentation](https://developers.mindee.com/docs/python-sdk)**.

## License
Copyright © Mindee

Available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).
